from flask import jsonify, make_response
from sqlalchemy.ext.asyncio import AsyncSession

import json

from ..responses.response import Response
from src.logger.logger import logger
from ..utils.currency_symbols import currency_symbols
from ..utils.jwt import JWT
from src.http_client.exhangerate import HTTPClientExchangeRate
from src.databases.models.currency import Currency
from src.databases.redis_client import redis_client


router_logger = logger.make_router_logger('exchange')
jwt_worker = JWT()


class CurrencyResponse(Response):
    @staticmethod
    async def symbol_currency_hand(request):
        symbol1 = request.args.get('symbol1').upper()
        symbol2 = request.args.get('symbol2').upper()
        symbol = symbol1 + symbol2
        response = make_response(jsonify({'message': f'{symbol} symbol is invalid'}), 422)
        condition = symbol1 in currency_symbols and symbol2 in currency_symbols
        if condition:
            data = await HTTPClientExchangeRate().get_symbol_price(symbol1, symbol2)
            if data:
                json_data = dict()
                json_data['price'] = float(data.get('quotes').get(symbol))
                json_data['price'] = f'{json_data['price']:.3f}'
                json_data['symbol'] = symbol
                response = make_response(jsonify(json_data), 200)
            return response
        return response

    async def all_currency_symbols_hand(self, session: AsyncSession, request):
        username = self.get_username(request)
        user_cached_id = f'currency_symbols:{username}'
        cached_data = await redis_client.get(user_cached_id)
        if cached_data:
            cached_data = json.loads(cached_data)
            response = make_response(jsonify(cached_data), 200)
            return response
        data = await Currency.get_all(session)
        json_data = self.serialize_data(data)
        await redis_client.set(user_cached_id, json.dumps(json_data))
        await redis_client.expire(user_cached_id, 300)
        response = make_response(jsonify(json_data), 200)
        return response
