from flask import jsonify, request, make_response

from ..utils.crypto_symbols import symbols
from ..utils.jwt import validate_bearer
from ..http_client.binance import HTTPClientBinance
from ..logger.logger import logger
from ..responses.response import Response


router_logger = logger.make_router_logger('Crypto')


class CryptoResponse(Response):
    @staticmethod
    async def symbol_crypto_hand_response(symbol):

        #po
        router_logger.info('Symbol')

        response = validate_bearer(request)
        if response != 'OK':
            return response
        response = make_response(jsonify({'message': f'{symbol} symbol is invalid'}), 422)
        try:
            symbol1, symbol2 = symbol.upper().split('_')
        except ValueError:
            return response
        condition = symbol1 in symbols and symbol2 in symbols
        if condition:
            symbol_ = symbol1 + symbol2
            data = await HTTPClientBinance().get_symbol_price(symbol_)
            if data:
                response = make_response(jsonify(data), 200)
            return response
        return response
