from flask import Blueprint, request, g

from ..responses.currency_response import CurrencyResponse, jwt_worker


router = Blueprint('currency', __name__)
response_maker = CurrencyResponse()


@router.before_request
async def currency_before_request_hand():
    response = await jwt_worker.validate_bearer(g.session, request)
    if response != 'OK':
        return response


@router.route('/symbol', methods=['GET'])
async def symbol_currency_hand():
    """
    Current price of symbol
    ---
    tags:
        - CURRENCY
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
        description: First symbol of currency symbol
        example: USD
      - name: symbol2
        in: query
        type: string
        required: true
        description: Second symbol of currency symbol
        example: UAH
    responses:
        200:
            description: Good request
            schema:
                type: object
                properties:
                    price:
                        type: string
                        description: latest price of the symbol
                        example: 41.1
                    symbol:
                      type: string
                      description: symbol that was given
                      example: USDUAH
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
    return await response_maker.symbol_currency_hand(request)


@router.route('/symbols/all', methods=['GET'])
async def all_currency_symbols_hand():
    """
    All world currencies
    ---
    tags:
        - CURRENCY
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
                            symbol: UAHUSD
                            symbol1: UAH
                            symbol2: USD
                    2:
                        type: number
                        description: Id of the symbol in database
                        example:
                            symbol: EURUSD
                            symbol1: EUR
                            symbol2: USD
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
    return await response_maker.all_currency_symbols_hand(session, request)
