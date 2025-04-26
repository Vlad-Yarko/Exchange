from sqlalchemy import Integer, String, select, insert, or_
from sqlalchemy.orm import Mapped, mapped_column

from typing import Optional

from src.databases.engine import main_session
from src.databases.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[bytes] = mapped_column()
    email: Mapped[str] = mapped_column(String(50), nullable=False)

    @classmethod
    async def register_user(cls, username: str, email: str, password: str = 'google') -> None:
        async with main_session() as session:
            await session.execute(insert(cls).values(
                username=username,
                password=password.encode(),
                email=email
            ))
            await session.commit()

    @classmethod
    async def is_user_by_username(cls, username: str) -> Optional['User']:
        async with main_session() as session:
            user = await session.execute(select(cls).where(cls.username == username))
            user = user.scalar()
            if user:
                return user
            return None

    @classmethod
    async def is_user_by_email(cls, email: str) -> Optional['User']:
        async with main_session() as session:
            user = await session.execute(select(cls).where(cls.email == email))
            user = user.scalar()
            if user:
                return user
            return None

