from sqlalchemy import select, delete, insert, and_
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


class Base(DeclarativeBase):
    @classmethod
    async def get_all(cls, session: AsyncSession):
        data = await session.execute(select(cls))
        clear_data = data.scalars().all()
        return clear_data

    @classmethod
    async def get_subscribes_by_user_id(cls, session: AsyncSession, used_id: int):
        data = await session.execute(select(cls).where(cls.user_id == used_id))
        if data:
            data = data.scalars().all()
        return data

    @classmethod
    async def get_symbol_by_symbol(cls, session: AsyncSession, symbol: str):
        data = await session.execute(select(cls).where(cls.symbol == symbol))
        if data:
            data = data.scalar()
        return data

    @classmethod
    async def make_subscribe(cls, session: AsyncSession,
                             symbol: str,
                             symbol1: str,
                             symbol2: str,
                             user_id: int,
                             symbol_id: int) -> None:
        await session.execute(insert(cls).values(
            symbol=symbol,
            symbol1=symbol1,
            symbol2=symbol2,
            user_id=user_id,
            symbol_id=symbol_id
        ))
        await session.commit()

    @classmethod
    async def remove_subscribe_by_user_id(cls, session: AsyncSession, user_id: int, symbol: str) -> None:
        await session.execute(delete(cls).where(and_(cls.user_id == user_id, cls.symbol == symbol)))
        await session.commit()
