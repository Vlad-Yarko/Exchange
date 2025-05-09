import re
import uuid
import random
import datetime

from flask import jsonify, make_response, url_for
from jwt import ExpiredSignatureError
from phonenumbers import NumberParseException
from sqlalchemy.ext.asyncio import AsyncSession

from ..responses.response import Response
from src.logger.logger import logger
from ..utils.email import Email
from ..utils.oauth import google
from ..utils.password import Password
from ..utils.jwt import JWT
from ..schemas.auth_schema import SignUpSchema, LogInEmailSchema, LogInUsernameSchema
from src.databases.redis_client import redis_client
from src.databases.models.web_user import WebUser


mail_maker = Email()
router_logger = logger.make_router_logger('AUTH')
password_worker = Password()
jwt_worker = JWT()


class AuthResponse(Response):

    @staticmethod
    async def is_refresh(request):
        response = 'OK'
        rt = request.cookies.get('refresh_token')
        # print('REFRESH', rt)
        if rt:
            response = make_response(jsonify(
                message='Refresh token has already found'
            ), 403)
        return response

    @staticmethod
    async def create_good_response(username):
        refresh_token = jwt_worker.create_refresh_token(username)
        response = make_response(jsonify(
            message='Correct credentials'
        ), 200)
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            secure=True,
            samesite='None',
            max_age=30 * 24 * 60 * 60
        )
        return response

    @staticmethod
    async def response_wrapper(func, request):
        try:
            response = await func(request)
            return response
        except ValueError as e:
            try:
                error_message = re.search(
                    r'Incorrect password|'
                    r'Invalid email adrress|'
                    r'Username has not found|'
                    r'Username is already taken|'
                    r'Email is already taken|'
                    r'Password must be between 8 and 70 characters|'
                    r'Username must be between 3 and 40 characters|'
                    r'Invalid email address|'
                    r'Email is not found|'
                    r'Username cannot contain spaces and @', str(e)).group(0)
            except AttributeError:
                error_message = 'server error'
            response = make_response(jsonify(
                message=error_message
            ), 422)
            return response
        except NumberParseException:
            response = make_response(jsonify(message='Phone number is invalid'), 422)
            return response

    async def signup(self, request):
        # cookies = request.cookies
        response = await self.is_refresh(request)
        if response != 'OK':
            return response
        # if cookies.get('redis-signup'):
        #     response = make_response(jsonify(message='Email code has already sent'), 403)
        #     return response
        form = request.form
        username = form.get('username')
        password = form.get('password')
        email = form.get('email')
        data = {
            'username': username,
            'password': password,
            'email': email
        }
        user = SignUpSchema(**data)
        await user.model_async_validate()
        code = random.randint(100000, 999999)
        await mail_maker.signup_mail(data.get('email'), code)
        password = password_worker.hash_password(password)
        user_id = str(uuid.uuid4())
        redis_id = f'user-signup:{user_id}'
        data['password'] = password
        data['code'] = code
        await redis_client.hset(redis_id, mapping=data)
        await redis_client.expire(redis_id, 60 * 5)
        response = make_response(jsonify(
            message='Good credentials, email was sent'
        ), 200)
        response.set_cookie(
            "redis-signup",
            user_id,
            httponly=True,
            secure=True,
            samesite='None',
            max_age=datetime.timedelta(minutes=5)
        )
        return response

    async def signup_hand(self, request):
        return await self.response_wrapper(self.signup, request)

    async def login_username(self, request):
        response = await self.is_refresh(request)
        if response != 'OK':
            return response
        form = request.form
        username = form.get('username')
        password = form.get('password')
        data = {
            'username': username,
            'password': password
        }
        user = LogInUsernameSchema(**data)
        await user.model_async_validate()
        return await self.create_good_response(username)

    async def login_email(self, session: AsyncSession, request):
        response = await self.is_refresh(request)
        if response != 'OK':
            return response
        form = request.form
        email = form.get('email')
        password = form.get('password')
        data = {
            'email': email,
            'password': password
        }
        user = LogInEmailSchema(**data)
        await user.model_async_validate()
        user = await WebUser.is_user_by_email(session, email)
        username = user.username
        return await self.create_good_response(username)

    async def login_username_hand(self, request):
        return await self.response_wrapper(self.login_username, request)

    async def login_email_hand(self, request):
        return await self.response_wrapper(self.login_email, request)

    @staticmethod
    async def google_login_hand(request):
        cookies = request.cookies
        refresh_token = cookies.get('refresh_token')
        if refresh_token:
            response = make_response(jsonify(message='You are already logged in'), 403)
            return response

        redirect_uri = url_for('auth.google_authorize_hand', _external=True)
        return google.authorize_redirect(redirect_uri)

    async def google_authorize_hand(self, session: AsyncSession, request):
        cookies = request.cookies
        refresh_token = cookies.get('refresh_token')
        if refresh_token:
            response = make_response(jsonify(message='You are already logged in'), 403)
            return response

        userinfo_endpoint = google.server_metadata['userinfo_endpoint']

        token = google.authorize_access_token()
        resp = google.get(userinfo_endpoint, token=token)
        user_info = resp.json()
        email = user_info.get('email')
        username = re.match(r'[^@]+@', email).group(0)
        user = await WebUser.is_user_by_email(session, email)
        if not user:
            await WebUser.register_web_user(
                session,
                username=username,
                email=email
            )
        return await self.create_good_response(username)

    @staticmethod
    async def logout_hand(request):
        refresh_token = request.cookies.get('refresh_token')
        if not refresh_token:
            response = make_response(jsonify(
                message='Refresh token has expired'
            ), 403)
            return response
        response = make_response(jsonify(
            message='Refresh token has deleted'
        ), 200)
        response.delete_cookie(
            "refresh_token",
            httponly=True,
            secure=True,
            samesite='None',
        )
        return response

    @staticmethod
    async def refresh_hand(request):
        cookies = request.cookies
        refresh_token = cookies.get('refresh_token')
        # print('REFRESH', refresh_token)
        response = make_response(jsonify(
            message='Refresh token has expired'
        ), 403)
        if not refresh_token:
            return response
        try:
            refresh_payload = jwt_worker.decode_token(refresh_token)
        except ExpiredSignatureError:
            return response
        access_token = jwt_worker.create_access_token(refresh_payload.get('sub'))
        response = make_response(jsonify(
            message='Refresh token is valid',
            bearerToken=access_token
        ))
        return response

    @staticmethod
    async def verify_mail_hand(session: AsyncSession, request):
        cookies = request.cookies
        refresh_token = cookies.get('refresh_token')
        if refresh_token:
            response = make_response(jsonify(message='You are already logged in'), 403)
            return response
        response = make_response(jsonify(message='Time to sign up has already passed'), 403)
        user_id = request.cookies.get('redis-signup')
        if not user_id:
            return response
        data = await redis_client.hgetall(f'user-signup:{user_id}')
        if not data:
            return response
        form = request.form
        server_code = data.get('code')
        user_code = form.get('code')
        if not server_code == user_code:
            response = make_response(jsonify(message='Entered code is invalid'), 422)
            return response
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        await redis_client.delete(f'user:{user_id}')
        response = make_response(jsonify(
            message='Good'
        ), 200)
        response.delete_cookie(
            "redis-signup",
            httponly=True,
            secure=True,
            samesite='None',
        )
        await WebUser.register_web_user(
            session,
            username=username,
            email=email,
            password=password.encode()
        )
        return response

    async def is_logged_in_hand(self, request):
        res = await self.is_refresh(request)
        if res == 'OK':
            message = False
        else:
            message = True
        response = make_response(jsonify(message=message), 200)
        return response
