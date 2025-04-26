from pydantic import BaseModel
from pydantic_async_validation import AsyncValidationModelMixin, async_field_validator

from ..databases.models.user import User
from ..utils.utils import check_password


class SignUpSchema(AsyncValidationModelMixin, BaseModel):
    username: str
    password: str
    email: str

    @async_field_validator('username')
    async def check_username(self, value):
        user = await User.is_user_by_username(value)
        if user:
            raise ValueError('Username is already taken')
        user = await User.is_user_by_email(self.email)
        if user:
            raise ValueError('Email is already taken')
        return value


class LogInSchema(AsyncValidationModelMixin, BaseModel):
    username: str
    password: str

    #
    @async_field_validator('username')
    async def check_credentials(self, value):
        user = await User.is_user_by_username(value)
        print('a')
        if user:
            print('b')
            if user.password == 'google'.encode() or not check_password(self.password, user.password):
                print('c')
                raise ValueError('Incorrect password')
            return value
        raise ValueError('Username has not found')
