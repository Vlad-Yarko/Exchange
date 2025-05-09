from flask import Blueprint, request, g

from ..responses.crypto_response import CryptoResponse, jwt_worker


router = Blueprint('crypto', __name__)
response_maker = CryptoResponse()


@router.before_request
async def crypto_before_request_hand():
    response = await jwt_worker.validate_bearer(g.session, request)
    if response != 'OK':
        return response


@router.route('/symbol', methods=['GET'])
async def symbol_crypto_hand():
    """
    Current price of symbol
    ---
    tags:
        - CRYPTO
    consumes:
        - application/json
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
        example: Bearer fajdfkjdsfkjldfdkdkgfhjwgh
      - name: symbol1
        in: query
        type: string
        required: true
        description: First symbol of crypto symbol
        example: BTC
      - name: symbol2
        in: query
        type: string
        required: true
        description: Second symbol of crypto symbol
        example: USDT
    responses:
        200:
            description: Good request
            schema:
                type: object
                properties:
                    price:
                        type: string
                        description: latest price of the symbol
                        example: 3.60000000
                    symbol:
                      type: string
                      description: symbol that was given
                      example: TONUSDT
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Access token is not valid
        422:
            description: Invalid data was sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: error message
                        example: poop symbol is invalid
        429:
            description: Suspicious activity
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Suspicious activity detected
    """
    return await response_maker.symbol_crypto_hand(request)


@router.route('/symbols/all', methods=['GET'])
async def all_crypto_symbols_hand():
    """
    All crypto currencies
    ---
    tags:
        - CRYPTO
    consumes:
        - application/json
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
        example: Bearer fajdfkjdsfkjldfdkdkgfhjwgh
    responses:
        200:
            description: Good request
            schema:
                type: object
                properties:
                    1:
                        type: number
                        description: Id of the symbol in database
                        example:
                            symbol: BTCUSDT
                            symbol1: BTC
                            symbol2: USDT
                    2:
                        type: number
                        description: Id of the symbol in database
                        example:
                            symbol: TONUSDT
                            symbol1: TON
                            symbol2: USDT
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Access token is not valid
        429:
            description: Suspicious activity
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Suspicious activity detected
    """
    session = g.session
    return await response_maker.all_crypto_symbols_hand(session, request)
