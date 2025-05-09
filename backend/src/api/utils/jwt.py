from datetime import datetime, timedelta, UTC

from flask import make_response, jsonify
from jwt import encode, decode
from jwt.exceptions import ExpiredSignatureError, DecodeError

from src.config import settings
from src.databases.models.web_user import WebUser


class JWT:
    @staticmethod
    def create_token(payload: dict):
        token = encode(
            payload=payload,
            key=settings.PRIVATE_KEY,
            algorithm='RS256'
        )
        return token

    @staticmethod
    def decode_token(token: str) -> dict:
        decoded_token = decode(
            jwt=token,
            key=settings.PUBLIC_KEY,
            algorithms=['RS256']
        )
        return decoded_token

    def create_access_token(self, username) -> str:
        now = datetime.now(UTC)
        iat = int(now.timestamp())
        exp = int((now + timedelta(minutes=15)).timestamp())
        payload = {
            'sub': username,
            'iat': iat,
            'exp': exp
        }
        token = self.create_token(payload)
        return token

    def create_refresh_token(self, username):
        now = datetime.now(UTC)
        iat = int(now.timestamp())
        exp = int((now + timedelta(days=32)).timestamp())
        payload = {
            'sub': username,
            'iat': iat,
            'exp': exp
        }
        token = self.create_token(payload)
        return token

    @staticmethod
    def parse_bearer(bearer_header) -> str:
        return bearer_header.split()[1]

    async def validate_bearer(self, session, request):
        bearer = request.headers.get('Authorization')
        if not bearer:
            response = make_response(jsonify(
                message='Access token is missing'
            ), 403)
            return response
        try:
            bearer = self.parse_bearer(bearer)
            payload = self.decode_token(bearer)
            username = payload.get('sub')
            response = 'OK'
            if not username:
                raise ValueError('')
            user = await WebUser.is_user_by_username(session, username)
            if not user:
                raise ValueError('')
        except (ExpiredSignatureError, DecodeError, ValueError, IndexError):
            response = make_response(jsonify(
                message='Access token is invalid'
            ), 403)
        return response

    def get_username(self, headers):
        try:
            bearer = self.parse_bearer(headers.get('Authorization'))
            payload = self.decode_token(bearer)
            username = payload.get('sub')
        except (ExpiredSignatureError, DecodeError, ValueError, IndexError):
            username = None
        return username

