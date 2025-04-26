from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv

import pathlib
from typing import ClassVar

BASE_DIR = pathlib.Path(__file__).parent
load_dotenv(find_dotenv())


class Settings(BaseSettings):
    DB: str
    CURRENCY_FREAKS_KEY: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    SECRET_KEY: str

    PRIVATE_KEY: ClassVar[str] = (BASE_DIR / 'keys/private_key.pem').read_text()
    PUBLIC_KEY: ClassVar[str] = (BASE_DIR / 'keys/public_key.pem').read_text()

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
# settings = Settings(
#     DB='postgresql+asyncpg://postgres:1234@localhost:5432/exchange',
#     EXCHANGE_API_KEY='79698e1fe78f404532bb6dec584ffcf9',
#     CURRENCY_FREAKS_KEY='1b9a97fa267d44a397ba940e01ec02b1'
# )

#EXCHANGE_API_KEY=79698e1fe78f404532bb6dec584ffcf9
# EXCHANGE_API_KEY: str
