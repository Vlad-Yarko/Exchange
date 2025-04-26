from flask import Blueprint

from ..responses.exchange_response import ExchangeResponse


router = Blueprint('exchange', __name__)
response_maker = ExchangeResponse()


@router.route('/symbol/<path:symbol>')
async def symbol_currency_hand(symbol):
    """
    World currency
    ---
    tags:
        - Currency
    consumes:
        - application/json
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token - Bearer {token}
      - name: symbol
        in: path
        type: string
        required: true
        description: Symbol of currency
        example: USD_UAH
    responses:
        200:
            description: Current price of symbol
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
        401:
            description: Access token is not valid
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Access token is not valid
        422:
            description: Invalid symbol
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: error message
                        example: poop symbol is invalid
    """
    return await response_maker.symbol_currency_hand_response(symbol)
