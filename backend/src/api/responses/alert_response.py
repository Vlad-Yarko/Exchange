from flask import make_response, jsonify
from sqlalchemy.ext.asyncio import AsyncSession

from src.logger.logger import logger
from ..responses.response import Response
from src.http_client.binance import HTTPClientBinance
from src.http_client.exhangerate import HTTPClientExchangeRate
from src.bot.bot import bot
from src.bot.messages.api_message import crypto_message, currency_message
from src.databases.models.tg_user import TelegramUser
from src.databases.models.crypto_subscribes import CryptoSubscribe
from src.databases.models.currency_subscribes import CurrencySubscribe


router_logger = logger.make_router_logger('ALERT')


class AlertResponse(Response):
    @staticmethod
    async def alert_all_hand(session: AsyncSession):
        crypto_subscribes = await CryptoSubscribe.get_all(session)
        currency_subscribes = await CurrencySubscribe.get_all(session)
        if not crypto_subscribes:
            response = make_response(jsonify(message='Crypto subscribes are empty'), 422)
            return response
        if not currency_subscribes:
            response = make_response(jsonify(message='Currency subscribes are empty'), 422)
            return response
        crypto_user_ids = set([subscribe.user_id for subscribe in crypto_subscribes])
        currency_user_ids = set([subscribe.user_id for subscribe in currency_subscribes])
        crypto_tg_users = await TelegramUser.get_users_by_user_ids(session, crypto_user_ids)
        currency_tg_users = await TelegramUser.get_users_by_user_ids(session, currency_user_ids)
        crypto_users = {}
        currency_users = {}
        for crypto_tg_user in crypto_tg_users:
            crypto_users[crypto_tg_user.user_id] = crypto_tg_user.chat_id
        for currency_tg_user in currency_tg_users:
            currency_users[currency_tg_user.user_id] = currency_tg_user.chat_id
        for subscribe in crypto_subscribes:
            symbol = subscribe.symbol
            data = await HTTPClientBinance().get_symbol_price(symbol)
            price = float(data.get('price'))
            price = f'{price:.3f}'
            await bot.send_message(
                chat_id=crypto_users[subscribe.user_id],
                text=crypto_message.render(symbol=symbol, price=price)
            )
        for subscribe in currency_subscribes:
            symbol = subscribe.symbol
            symbol1 = subscribe.symbol1
            symbol2 = subscribe.symbol2
            data = await HTTPClientExchangeRate().get_symbol_price(symbol1, symbol2)
            price = float(data.get('quotes').get(symbol))
            price = f'{price:.3f}'
            await bot.send_message(
                chat_id=currency_users[subscribe.user_id],
                text=currency_message.render(symbol=symbol, price=price)
            )
        response = make_response(jsonify(message='Subscribed users were alerted'), 200)
        return response
