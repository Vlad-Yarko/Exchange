from typing import Optional, Union

from sqlalchemy import Integer, String, select, insert, ForeignKey, update
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base import Base


class WebUser(Base):
    __tablename__ = 'web_users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    phone_number: Mapped[str] = mapped_column(ForeignKey('telegram_users.phone_number'), nullable=True, unique=True)

    @classmethod
    async def register_web_user(cls, session: AsyncSession, username: str, email: str, password: Union[str, bytes] = 'google') -> None:
        if password == 'google':
            password = password.encode()
        await session.execute(insert(cls).values(
            username=username,
            password=password,
            email=email
        ))
        await session.commit()

    @classmethod
    async def is_user_by_username(cls, session: AsyncSession, username: str) -> Optional['WebUser']:
        user = await session.execute(select(cls).where(cls.username == username))
        user = user.scalar()
        if user:
            return user
        return None

    @classmethod
    async def is_user_by_email(cls, session: AsyncSession, email: str) -> Optional['WebUser']:
        user = await session.execute(select(cls).where(cls.email == email))
        user = user.scalar()
        if user:
            return user
        return None

    @classmethod
    async def is_user_by_phonenumber(cls, session: AsyncSession, phone_number: str) -> Optional['WebUser']:
        user = await session.execute(select(cls).where(cls.phone_number == phone_number))
        user = user.scalar()
        if user:
            return user
        return None

    @classmethod
    async def update_username_by_username(cls, session: AsyncSession, current_username: str, new_username: str) -> None:
        await session.execute(update(cls).values(
            username=new_username
        ).where(cls.username == current_username))
        await session.commit()

    @classmethod
    async def update_password_by_username(cls, session: AsyncSession, username, new_password) -> None:
        await session.execute(update(cls).values(
            password=new_password
        ).where(cls.username == username))
        await session.commit()

    @classmethod
    async def update_phonenumber_by_username(cls, session: AsyncSession, username, new_phonenumber) -> None:
        await session.execute(update(cls).values(
            phone_number=new_phonenumber.strip('+')
        ).where(cls.username == username))
        await session.commit()

    @classmethod
    async def remove_phone_number_by_username(cls, session: AsyncSession, username) -> None:
        await session.execute(update(cls).values(
            phone_number=None
        ).where(cls.username == username))
        await session.commit()
