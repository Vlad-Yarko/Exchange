from typing import Optional

from sqlalchemy import Integer, String, select, insert, BigInteger, ForeignKey, update
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base import Base


class TelegramUser(Base):
    __tablename__ = 'telegram_users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('web_users.id'), nullable=True)

    # crypto_subscribes: Mapped[int] = mapped_column(ForeignKey('crypto_subscribes.id'), nullable=True)
    # currency_subscribes: Mapped[int] = mapped_column(ForeignKey('currency_subscribes.id'), nullable=True)

    @classmethod
    async def is_user_by_chat_id(cls, session: AsyncSession, chat_id: int) -> Optional['TelegramUser']:
        user = await session.execute(select(cls).where(cls.chat_id == chat_id))
        user = user.scalar()
        if user:
            return user
        return None

    @classmethod
    async def register_tg_user(cls, session: AsyncSession, chat_id, phone_number) -> None:
        await session.execute(insert(cls).values(
            chat_id=chat_id,
            phone_number=phone_number
        ))
        await session.commit()

    @classmethod
    async def is_user_by_user_id(cls, session: AsyncSession, used_id: int) -> Optional['TelegramUser']:
        user = await session.execute(select(cls).where(cls.user_id == used_id))
        user = user.scalar()
        if user:
            return user
        return None

    @classmethod
    async def is_user_by_phone_number(cls, session: AsyncSession, phone_number: str) -> Optional['TelegramUser']:
        user = await session.execute(select(cls).where(cls.phone_number == phone_number.strip('+')))
        user = user.scalar()
        if user:
            return user
        return None

    @classmethod
    async def update_user_id_by_phone_number(cls, session: AsyncSession, phone_number: str, user_id: int) -> None:
        await session.execute(update(cls).where(cls.phone_number == phone_number.strip('+')).values(
            user_id=user_id
        ))
        await session.commit()

    @classmethod
    async def remove_user_id_by_user_id(cls, session: AsyncSession, user_id: int) -> None:
        await session.execute(update(cls).where(cls.user_id == user_id).values(
            user_id=None
        ))
        await session.commit()

    @classmethod
    async def get_users_by_user_ids(cls, session: AsyncSession, user_ids: set[int]):
        data = await session.execute(select(cls).where(cls.user_id.in_(user_ids)))
        if data:
            data = data.scalars().all()
        return data
