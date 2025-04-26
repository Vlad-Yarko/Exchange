from flask import jsonify, request, make_response

from ..utils.jwt import validate_bearer
from ..utils.currency_symbols import symbols
from ..http_client.exhangerate import HTTPClientExchangeRate
from ..logger.logger import logger
from ..responses.response import Response


router_logger = logger.make_router_logger('exchange')


class ExchangeResponse(Response):
    @staticmethod
    async def symbol_currency_hand_response(symbol):

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
            data = await HTTPClientExchangeRate().get_symbol_price(symbol1, symbol2)
            if data:
                response = make_response(jsonify(data), 200)
            return response
        return response
