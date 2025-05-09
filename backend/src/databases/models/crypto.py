from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..models.base import Base


class Crypto(Base):
    __tablename__ = 'crypto'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False)
    symbol1: Mapped[str] = mapped_column(String(50), nullable=False)
    symbol2: Mapped[str] = mapped_column(String(50), nullable=False)
