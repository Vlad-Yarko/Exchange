from flask import jsonify, request, make_response, url_for
from jwt import ExpiredSignatureError
from pydantic import ValidationError

import re
import uuid
import random
import datetime

from ..utils.email import Email
from ..utils.oauth import google
from ..schemas.auth_schema import SignUpSchema, LogInSchema
from ..utils.utils import hash_password
from ..databases.models.user import User
from ..utils.jwt import create_refresh_token, create_access_token, decode_token
from ..databases.redis_client import redis_client
from ..logger.logger import logger
from ..responses.response import Response


mail_maker = Email()
router_logger = logger.make_router_logger('AUTH')


class AuthResponse(Response):
    @staticmethod
    async def signup_hand_response():

        # po
        router_logger.info('Sign up')

        cookies = request.cookies
        refresh_token = cookies.get('refresh_token')
        if refresh_token:
            response = make_response(jsonify(message='You are already logged in'), 403)
            return response
        if cookies.get('redis'):
            response = make_response(jsonify(message='Email code has already sent'), 403)
            return response
        form = request.form
        username = form.get('username')
        password = form.get('password')
        email = form.get('email')
        data = {
            'username': username,
            'password': password,
            'email': email
        }
        try:
            user = SignUpSchema(**data)
            await user.model_async_validate()
            code = random.randint(100000, 999999)
            await mail_maker.signup_mail(data.get('email'), code)
            password = hash_password(password)
            user_id = str(uuid.uuid4())
            redis_id = f'user:{user_id}'
            data['password'] = password
            data['code'] = code
            await redis_client.hset(redis_id, mapping=data)
            await redis_client.expire(redis_id, 60 * 5)
            response = make_response(jsonify(
                message='Good credentials, email was sent'
            ), 200)
            response.set_cookie(
                "redis",
                user_id,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=datetime.timedelta(minutes=5)
            )
            return response
        except ValidationError as e:
            error_message = re.search(r'Username is already taken|Email is already taken', str(e))
            if error_message is None:
                error_message = 'Incorrect email address'
            else:
                error_message = error_message.group(0)
            response = make_response(jsonify(
                message=error_message
            ), 422)
            return response

    @staticmethod
    async def login_hand_response():

        # po
        router_logger.info('Login')

        rt = request.cookies.get('refresh_token')
        if rt:
            response = make_response(jsonify(
                message='Refresh token has already found'
            ), 403)
            return response
        form = request.form
        username = form.get('username')
        password = form.get('password')
        data = {
            'username': username,
            'password': password
        }
        try:
            user = LogInSchema(**data)
            await user.model_async_validate()
            refresh_token = create_refresh_token(username)
            response = make_response(jsonify(
                message='Good'
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
        except ValueError as e:
            try:
                error_message = re.search(r'Incorrect password|Username has not found', str(e)).group(0)
            except AttributeError:
                error_message = 'Server error'
            response = make_response(jsonify(
                message=error_message
            ), 422)
            return response

    @staticmethod
    async def google_login_hand_response():

        # po
        router_logger.info('Google login')

        cookies = request.cookies
        refresh_token = cookies.get('refresh_token')
        if refresh_token:
            response = make_response(jsonify(message='You are already logged in'), 403)
            return response

        redirect_uri = url_for('auth.google_authorize_hand', _external=True)
        return google.authorize_redirect(redirect_uri)

    @staticmethod
    async def google_authorize_hand_response():

        # po
        router_logger.info('Google authorize')

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
        user = await User.is_user_by_username(username)
        if not user:
            await User.register_user(
                username=username,
                email=email
            )
        refresh_token = create_refresh_token(username)
        response = make_response(jsonify(
            message='Good login'
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
    async def logout_hand_response():

        # po
        router_logger.info('Logout')

        refresh_token = request.cookies.get('refresh_token')
        if not refresh_token:
            # Refresh token is already expired or missing
            response = make_response(jsonify(
                message='You are not logged in'
            ), 401)
            return response
        response = make_response(jsonify(
            message='You logged out successfully'
        ), 200)
        response.delete_cookie(
            "refresh_token",
            httponly=True,
            secure=True,
            samesite='None',
        )
        return response

    @staticmethod
    async def refresh_hand_response():

        # po
        router_logger.info('Refresh')

        cookies = request.cookies
        refresh_token = cookies.get('refresh_token')
        if not refresh_token:
            response = make_response(jsonify(
                message='Refresh token is missing'
            ), 401)
            return response
        try:
            refresh_payload = decode_token(refresh_token)
        except ExpiredSignatureError:
            response = make_response(jsonify(
                message='Refresh token is expired'
            ), 403)
            return response
        access_token = create_access_token(refresh_payload.get('sub'))
        response = make_response(jsonify(
            message='Refresh token is valid',
            bearerToken=access_token
        ))
        return response

    @staticmethod
    async def verify_mail_hand_response():

        # po
        router_logger.info('Verify mail')

        cookies = request.cookies
        refresh_token = cookies.get('refresh_token')
        if refresh_token:
            response = make_response(jsonify(message='You are already logged in'), 403)
            return response
        response = make_response(jsonify(message='Time to sign up has already passed'), 403)
        user_id = request.cookies.get('redis')
        if not user_id:
            return response
        data = await redis_client.hgetall(f'user:{user_id}')
        if not data:
            return response
        form = request.form
        server_code = data.get('code')
        user_code = form.get('code')
        if not server_code == user_code:
            response = make_response(jsonify(message='Incorrect email code entered'), 422)
            return response
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        await redis_client.delete(f'user:{user_id}')
        response = make_response(jsonify(
            message='Good'
        ), 200)
        response.delete_cookie(
            "redis",
            httponly=True,
            secure=True,
            samesite='None',
        )
        await User.register_user(
            username=username,
            email=email,
            password=password
        )
        return response
