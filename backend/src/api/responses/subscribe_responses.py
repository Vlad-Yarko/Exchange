from flask import make_response, jsonify
from sqlalchemy.ext.asyncio import AsyncSession

from src.logger.logger import logger
from ..responses.response import Response
from ..utils.jwt import JWT
from ..utils.crypto_symbols import crypto_symbols
from ..utils.currency_symbols import currency_symbols
from src.databases.models.web_user import WebUser
from src.databases.models.crypto_subscribes import CryptoSubscribe
from src.databases.models.currency_subscribes import CurrencySubscribe
from src.databases.models.currency import Currency
from src.databases.models.crypto import Crypto


router_logger = logger.make_router_logger('SUBSCRIBE')
jwt_worker = JWT()


class SubscribeResponse(Response):
    @staticmethod
    def get_symbols(request) -> tuple[str, str, str]:
        queries = request.args
        symbol1 = queries.get('symbol1').upper()
        symbol2 = queries.get('symbol2').upper()
        symbol = symbol1 + symbol2
        return symbol1, symbol2, symbol

    async def check_phone_number_before_request_hand(self, session: AsyncSession, request):
        response = 'OK'
        username = self.get_username(request)
        user = await WebUser.is_user_by_username(session, username)
        if not user.phone_number:
            response = make_response(jsonify(message='You do not have phone number registered'), 403)
            return response
        return response

    async def crypto_subscribe_before(self, request):
        response = 'OK'
        symbol1, symbol2, symbol = self.get_symbols(request)
        if symbol1 not in crypto_symbols or symbol2 not in crypto_symbols:
            response = make_response(jsonify(message=f'Invalid symbol - {symbol}'), 422)
        return response

    async def currency_subscribe_before(self, request):
        response = 'OK'
        symbol1, symbol2, symbol = self.get_symbols(request)
        if symbol1 not in currency_symbols or symbol2 not in currency_symbols:
            response = make_response(jsonify(message=f'Invalid symbol - {symbol}'), 422)
        return response

    async def crypto_make_subscribe(self, session: AsyncSession, request):
        username = self.get_username(request)
        symbol1, symbol2, symbol = self.get_symbols(request)
        user = await WebUser.is_user_by_username(session, username)
        subscribes = await CryptoSubscribe.get_subscribes_by_user_id(session, user.id)
        i = False
        for subscribe in subscribes:
            if subscribe.symbol == symbol:
                i = True
                break
        if i:
            response = make_response(jsonify(message='Subscribe has already made'), 403)
            return response
        symbol_data = await Crypto.get_symbol_by_symbol(session, symbol)
        data = {
            'symbol': symbol,
            'symbol1': symbol1,
            'symbol2': symbol2,
            'user_id': user.id,
            'symbol_id': symbol_data.id
        }
        await CryptoSubscribe.make_subscribe(session, **data)
        response = make_response(jsonify(message='Subscribe has made'), 200)
        return response

    async def crypto_remove_subscribe(self, session: AsyncSession, request):
        username = self.get_username(request)
        symbol1, symbol2, symbol = self.get_symbols(request)
        user = await WebUser.is_user_by_username(session, username)
        subscribes = await CryptoSubscribe.get_subscribes_by_user_id(session, user.id)
        if not subscribes:
            response = make_response(jsonify(message='You do not have any subscribes'), 403)
            return response
        for subscribe in subscribes:
            if subscribe.symbol == symbol:
                await CryptoSubscribe.remove_subscribe_by_user_id(session, user.id, symbol)
                response = make_response(jsonify(message='Subscribe has removed'), 200)
                return response
        response = make_response(jsonify(message=f'Symbol {symbol} has not found in subscribes'), 422)
        return response

    async def currency_make_subscribe(self, session: AsyncSession, request):
        username = self.get_username(request)
        symbol1, symbol2, symbol = self.get_symbols(request)
        user = await WebUser.is_user_by_username(session, username)
        subscribes = await CurrencySubscribe.get_subscribes_by_user_id(session, user.id)
        i = False
        for subscribe in subscribes:
            if subscribe.symbol == symbol:
                i = True
                break
        if i:
            response = make_response(jsonify(message='Subscribe has already made'), 403)
            return response
        symbol_data = await Currency.get_symbol_by_symbol(session, symbol)
        data = {
            'symbol': symbol,
            'symbol1': symbol1,
            'symbol2': symbol2,
            'user_id': user.id,
            'symbol_id': symbol_data.id
        }
        await CurrencySubscribe.make_subscribe(session, **data)
        response = make_response(jsonify(message='Subscribe has made'), 200)
        return response

    async def currency_remove_subscribe(self, session: AsyncSession, request):
        username = self.get_username(request)
        symbol1, symbol2, symbol = self.get_symbols(request)
        user = await WebUser.is_user_by_username(session, username)
        subscribes = await CurrencySubscribe.get_subscribes_by_user_id(session, user.id)
        if not subscribes:
            response = make_response(jsonify(message='You do not have any subscribes'), 422)
            return response
        for subscribe in subscribes:
            if subscribe.symbol == symbol:
                await CurrencySubscribe.remove_subscribe_by_user_id(session, user.id, symbol)
                response = make_response(jsonify(message='Subscribe has removed'), 200)
                return response
        response = make_response(jsonify(message=f'Symbol {symbol} has not found in subscribes'), 422)
        return response
