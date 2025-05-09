from flask import jsonify, make_response
from sqlalchemy.ext.asyncio import AsyncSession

import json

from ..responses.response import Response
from src.logger.logger import logger
from ..utils.crypto_symbols import crypto_symbols
from ..utils.jwt import JWT
from src.http_client.binance import HTTPClientBinance
from src.databases.models.crypto import Crypto
from src.databases.redis_client import redis_client


router_logger = logger.make_router_logger('Crypto')
jwt_worker = JWT()


class CryptoResponse(Response):
    @staticmethod
    async def symbol_crypto_hand(request):
        symbol1 = request.args.get('symbol1').upper()
        symbol2 = request.args.get('symbol2').upper()
        symbol = symbol1 + symbol2
        response = make_response(jsonify({'message': f'{symbol} symbol is invalid'}), 422)
        condition = symbol1 in crypto_symbols and symbol2 in crypto_symbols
        if condition:
            symbol_ = symbol1 + symbol2
            data = await HTTPClientBinance().get_symbol_price(symbol_)
            data['price'] = f'{float(data['price']):.3f}'
            if data:
                response = make_response(jsonify(data), 200)
            return response
        return response

    async def all_crypto_symbols_hand(self, session: AsyncSession, request):
        username = self.get_username(request)
        user_cached_id = f'crypto_symbols:{username}'
        cached_data = await redis_client.get(user_cached_id)
        if cached_data:
            cached_data = json.loads(cached_data)
            response = make_response(jsonify(cached_data), 200)
            return response
        data = await Crypto.get_all(session)
        json_data = self.serialize_data(data)
        await redis_client.set(user_cached_id, json.dumps(json_data))
        await redis_client.expire(user_cached_id, 300)
        response = make_response(jsonify(json_data), 200)
        return response
