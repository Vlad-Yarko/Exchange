import re

from pydantic import BaseModel, field_validator
from pydantic_async_validation import AsyncValidationModelMixin, async_field_validator

from src.databases.engine import main_session
from src.databases.models.web_user import WebUser
from ..utils.password import Password


password_worker = Password()


def check_pw(password):
    password_length = len(password)
    if password_length < 8 or password_length > 70:
        raise ValueError('Password must be between 8 and 70 characters')
    return password


async def check_us(username):
    username_length = len(username)
    if username_length < 3 or username_length > 40:
        raise ValueError('Username must be between 3 and 40 characters')
    if ' ' in username or '@' in username:
        raise ValueError('Username cannot contain spaces and @')
    return username


async def check_e(email):
    is_valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    if not is_valid_email:
        raise ValueError('Invalid email address')
    return email


class SignUpSchema(AsyncValidationModelMixin, BaseModel):
    username: str
    password: str
    email: str

    @field_validator('password')
    @classmethod
    def check_password(cls, value):
        return check_pw(value)

    @async_field_validator('username')
    async def check_username(self, value):
        await check_us(value)
        await check_e(self.email)
        async with main_session() as session:
            user = await WebUser.is_user_by_username(session, value)
            if user:
                raise ValueError('Username is already taken')
            user = await WebUser.is_user_by_email(session, self.email)
            if user:
                raise ValueError('Email is already taken')
            return value


class LogInUsernameSchema(AsyncValidationModelMixin, BaseModel):
    username: str
    password: str

    @field_validator('password')
    @classmethod
    def check_password(cls, value):
        return check_pw(value)

    @async_field_validator('username')
    async def check_credentials(self, value):
        await check_us(value)
        async with main_session() as session:
            user = await WebUser.is_user_by_username(session, value)
            if not user:
                raise ValueError('Username has not found')
            if user.password == 'google'.encode() or not password_worker.check_password(self.password, user.password):
                raise ValueError('Incorrect password')
            return value


class LogInEmailSchema(AsyncValidationModelMixin, BaseModel):
    email: str
    password: str

    @field_validator('password')
    @classmethod
    def check_password(cls, value):
        return check_pw(value)

    @async_field_validator('email')
    async def check_email(self, value):
        await check_e(self.email)
        async with main_session() as session:
            user = await WebUser.is_user_by_email(session, value)
            if not user:
                raise ValueError('Email is not found')
            if user.password == 'google'.encode() or not password_worker.check_password(self.password, user.password):
                raise ValueError('Incorrect password')
            return user
