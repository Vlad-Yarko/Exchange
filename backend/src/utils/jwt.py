from flask import make_response, jsonify
from jwt import encode, decode
from jwt.exceptions import ExpiredSignatureError, DecodeError

from datetime import datetime, timedelta, UTC

from ..config import settings


def create_token(payload: dict):
    token = encode(
        payload=payload,
        key=settings.PRIVATE_KEY,
        algorithm='RS256'
    )
    return token


def decode_token(token: str) -> dict:
    decoded_token = decode(
        jwt=token,
        key=settings.PUBLIC_KEY,
        algorithms=['RS256']
    )
    return decoded_token


def create_access_token(username) -> str:
    now = datetime.now(UTC)
    iat = int(now.timestamp())
    exp = int((now + timedelta(minutes=15)).timestamp())
    payload = {
        'sub': username,
        'iat': iat,
        'exp': exp
    }
    token = create_token(payload)
    return token


def create_refresh_token(username):
    now = datetime.now(UTC)
    iat = int(now.timestamp())
    exp = int((now + timedelta(days=32)).timestamp())
    payload = {
        'sub': username,
        'iat': iat,
        'exp': exp
    }
    token = create_token(payload)
    return token


def validate_bearer(request):
    bearer = request.headers.get('Authorization')
    if not bearer:
        response = make_response(jsonify(
            message='Access token is missing'
        ), 401)
        return response
    try:
        bearer = bearer.split()[1]
        payload = decode_token(bearer)
        username = payload.get('sub')
        response = 'OK'
        if not username:
            raise ValueError('')
    except (ExpiredSignatureError, DecodeError, ValueError, IndexError):
        response = make_response(jsonify(
            message='Access token is invalid'
        ), 401)
    return response
