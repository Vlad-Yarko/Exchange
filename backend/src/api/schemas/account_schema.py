from pydantic import BaseModel, field_validator
from pydantic_async_validation import AsyncValidationModelMixin, async_field_validator
import phonenumbers

from src.databases.engine import main_session
from src.databases.models.web_user import WebUser
from src.databases.models.tg_user import TelegramUser


class AccountPasswordSchema(BaseModel):
    password: str

    @field_validator('password')
    @classmethod
    def check_password(cls, value):
        password_length = len(value)
        if password_length < 8 or password_length > 70:
            raise ValueError('Password must be between 8 and 70 characters')
        return value


class AccountUsernameSchema(AsyncValidationModelMixin, BaseModel):
    username: str

    @field_validator('username')
    @classmethod
    def check_username_sync(cls, value):
        username_length = len(value)
        if username_length < 3 or username_length > 40:
            raise ValueError('Username must be between 3 and 40 characters')
        if ' ' in value or '@' in value:
            raise ValueError('Username cannot contain spaces and @')
        return value

    @async_field_validator('username')
    async def check_username(self, value):
        async with main_session() as session:
            user = await WebUser.is_user_by_username(session, value)
            if user:
                raise ValueError('Username is already taken')
            return value


class AccountPhoneNumberSchema(AsyncValidationModelMixin, BaseModel):
    username: str
    phone_number: str

    @field_validator('phone_number')
    @classmethod
    def check_phonenumber(cls, value):
        parsed_number = phonenumbers.parse(value)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError('Entered phone number is invalid')
        return value

    @async_field_validator('phone_number')
    async def check_phonenumber_async(self, value):
        async with main_session() as session:
            tg_user = await TelegramUser.is_user_by_phone_number(session, value)
            if not tg_user:
                raise ValueError('Phone number was not found')
            return tg_user
