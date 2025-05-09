from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..models.base import Base


class CryptoSubscribe(Base):
    __tablename__ = 'crypto_subscribes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False)
    symbol1: Mapped[str] = mapped_column(String(50), nullable=False)
    symbol2: Mapped[str] = mapped_column(String(50), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('web_users.id'))
    symbol_id: Mapped[int] = mapped_column(ForeignKey('crypto.id'))
