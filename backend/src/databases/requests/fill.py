import asyncio

from src.databases.models.crypto import Crypto
from src.databases.models.currency import Currency
from src.databases.engine import main_session
from src.api.utils.crypto_symbols import crypto_symbols
from src.api.utils.currency_symbols import currency_symbols


async def fill_crypto():
    async with main_session() as session:
        symbols = [
            Crypto(symbol=f"{name}USDT", symbol1=name, symbol2="USDT")
            for name in crypto_symbols
        ]
        session.add_all(symbols)
        await session.commit()


async def fill_currency():
    async with main_session() as session:
        symbols = []
        for i in range(len(currency_symbols)):
            symbol1 = currency_symbols[i]
            for j in range(len(currency_symbols)):
                symbol2 = currency_symbols[j]
                symbols.append(Currency(symbol=f"{symbol1}{symbol2}", symbol1=symbol1, symbol2=symbol2))
        session.add_all(symbols)
        await session.commit()


async def fill():
    await fill_crypto()
    await fill_currency()


asyncio.run(fill())
