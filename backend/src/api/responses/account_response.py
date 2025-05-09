import re
import random
import json

from flask import jsonify, make_response
from phonenumbers import NumberParseException
from sqlalchemy.ext.asyncio import AsyncSession

from ..responses.response import Response
from src.logger.logger import logger
from src.bot.bot import bot
from src.bot.messages.api_message import code_message
from ..utils.email import Email
from ..utils.jwt import JWT
from ..utils.password import Password
from ..schemas.account_schema import AccountUsernameSchema, AccountPhoneNumberSchema, AccountPasswordSchema
from src.databases.redis_client import redis_client
from src.databases.models.web_user import WebUser
from src.databases.models.tg_user import TelegramUser


mail_maker = Email()
router_logger = logger.make_router_logger('ACCOUNT')
password_worker = Password()
jwt_worker = JWT()


class AccountResponse(Response):

    async def is_email_validated(self, request):
        username = self.get_username(request)
        if not await redis_client.get(f'user-validated:{username}'):
            response = make_response(jsonify(message='Email is not validated'), 403)
            return response
        return 'OK'

    async def send_account_email_hand(self, session: AsyncSession, request):
        username = self.get_username(request)
        user = await WebUser.is_user_by_username(session, username)
        if not user:
            response = make_response(jsonify(message='Access token is invalid'), 403)
            return response
        email = user.email
        code = random.randint(100000, 999999)
        await mail_maker.change_credentials_mail(email, code)
        await redis_client.setex(f'user-validate:{username}', 300, code)
        response = make_response(jsonify(message='Email was sent'), 200)
        return response

    async def validate_account_email_hand(self, request):
        username = self.get_username(request)
        server_code = await redis_client.get(f'user-validate:{username}')
        if not server_code:
            response = make_response(jsonify(message='Time to validate has already passed'), 403)
            return response
        user_code = request.form.get('code')
        if user_code != server_code:
            response = make_response(jsonify(message='Entered code is invalid'), 422)
            return response
        await redis_client.delete(f'user-validate:{username}')
        await redis_client.setex(f'user-validated:{username}', 300, 'true')
        response = make_response(jsonify(message='Entered code was correct'), 200)
        return response

    async def change_account_username_hand(self, session: AsyncSession, request):
        response = await self.is_email_validated(request)
        if response != 'OK':
            return response
        try:
            new_username = request.form.get('username')
            user = AccountUsernameSchema(username=new_username)
            current_username = self.get_username(request)
            await user.model_async_validate()
            await WebUser.update_username_by_username(session, current_username, new_username)
            await redis_client.delete(f'user-validated:{current_username}')
            response = make_response(jsonify(message='Username has changed'), 200)
            refresh_token = jwt_worker.create_refresh_token(new_username)
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=30 * 24 * 60 * 60
            )
            return response
        except ValueError as e:
            error_message = re.search(r'Username must be between 3 and 40 characters|'
                                      r'Username is already taken|'
                                      r'Username cannot contain spaces and @', str(e)).group(0)
            response = make_response(jsonify(message=error_message), 422)
            return response

    async def change_account_password_hand(self, session: AsyncSession, request):
        response = await self.is_email_validated(request)
        if response != 'OK':
            return response
        username = self.get_username(request)
        new_password = request.form.get('password')
        try:
            AccountPasswordSchema(password=new_password)
            hashed_password = password_worker.hash_password(new_password)
            await WebUser.update_password_by_username(session, username, hashed_password)
            await redis_client.delete(f'user-validated:{username}')
            response = make_response(jsonify(message='Password has changed'), 200)
            return response
        except ValueError:
            response = make_response(jsonify(message='Password must be between 8 and 70 characters'), 422)
            return response

    async def send_phone_number_hand(self, session: AsyncSession, request):
        username = self.get_username(request)
        new_phone_number = request.form.get('phoneNumber')
        try:
            u = AccountPhoneNumberSchema(phone_number=new_phone_number, username=username)
            await u.model_async_validate()
            code = random.randint(100000, 999999)
            tg_user = await TelegramUser.is_user_by_phone_number(session, new_phone_number)
            data = {
                'code': code,
                'phone_number': new_phone_number
            }
            await redis_client.set(f'user-telegram:{username}', json.dumps(data))
            await redis_client.expire(f'user-telegram:{username}', 300)
            await bot.send_message(chat_id=tg_user.chat_id, text=code_message.render(username=username, code=code))
            response = make_response(jsonify(message='Code was sent via telegram'))
            return response
        except NumberParseException:
            response = make_response(jsonify(message='Entered invalid phone number'), 422)
            return response
        except ValueError as e:
            error_message = re.search(r'Phone number was not found|Entered phone number is invalid', str(e)).group(0)
            response = make_response(jsonify(message=error_message), 422)
            return response

    async def verify_new_phone_number_hand(self, session: AsyncSession, request):
        username = self.get_username(request)
        data = await redis_client.get(f'user-telegram:{username}')
        if not data:
            response = make_response(jsonify(message='Code was not sent'), 403)
            return response
        data = json.loads(data)
        server_code = int(data.get('code'))
        try:
            user_code = int(request.form.get('code'))
            if server_code != user_code:
                raise ValueError('')
        except ValueError:
            response = make_response(jsonify(message='Invalid code sent'), 403)
            return response
        phone_number = data.get('phone_number')
        await WebUser.update_phonenumber_by_username(session, username, phone_number)
        user = await WebUser.is_user_by_username(session, username)
        await TelegramUser.update_user_id_by_phone_number(session, phone_number, user.id)
        await redis_client.delete(f'user-telegram:{username}')
        response = make_response(jsonify(message='Phone number has been changed'))
        return response

    async def remove_account_phone_number_hand(self, session: AsyncSession, request):
        username = self.get_username(request)
        user = await WebUser.is_user_by_username(session, username)
        if not user.phone_number:
            response = make_response(jsonify(message='Phone number has not found'), 403)
            return response
        user = await WebUser.is_user_by_username(session, username)
        await WebUser.remove_phone_number_by_username(session, username)
        await TelegramUser.remove_user_id_by_user_id(session, user.id)
        response = make_response(jsonify(message='Phone number has removed'), 200)
        return response

    async def account_info_hand(self, session: AsyncSession, request):
        username = self.get_username(request)
        user = await WebUser.is_user_by_username(session, username)
        email = user.email
        data = {
            'username': username,
            'email': email
        }
        response = make_response(jsonify(**data), 200)
        return response
