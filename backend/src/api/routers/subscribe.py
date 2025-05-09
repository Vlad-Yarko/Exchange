from flask import Blueprint, g, request

from ..responses.subscribe_responses import SubscribeResponse, jwt_worker


router = Blueprint('subscribe', __name__)
response_maker = SubscribeResponse()


@router.before_request
async def subscribe_before_request_hand():
    response = await jwt_worker.validate_bearer(g.session, request)
    if response != 'OK':
        return response


@router.before_request
async def check_phone_number_before_request_hand():
    response = await response_maker.check_phone_number_before_request_hand(g.session, request)
    if response != 'OK':
        return response


@router.before_request
async def crypto_subscribe_before():
    if request.endpoint in ('subscribe.crypto_make_subscribe', 'subscribe.crypto_remove_subscribe'):
        response = await response_maker.crypto_subscribe_before(request)
        if response != 'OK':
            return response


@router.before_request
async def currency_subscribe_before():
    if request.endpoint in ('subscribe.currency_make_subscribe', 'subscribe.currency_remove_subscribe'):
        response = await response_maker.currency_subscribe_before(request)
        if response != 'OK':
            return response


@router.route('/crypto/make', methods=['POST'])
async def crypto_make_subscribe():
    """
    Make crypto subscribe
    ---
    tags:
        - SUBSCRIBE
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
                    message:
                        type: string
                        description: API message
                        example: Subscribe has made
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Subscribe has already made
        422:
            description: Invalid data sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Invalid symbol - poop
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
    return await response_maker.crypto_make_subscribe(session, request)


@router.route('/crypto/remove', methods=['DELETE'])
async def crypto_remove_subscribe():
    """
    Remove crypto subscribe
    ---
    tags:
        - SUBSCRIBE
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
                    message:
                        type: string
                        description: API message
                        example: Subscribe has removed
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: You do not have any subscribes
        422:
            description: Invalid data sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Symbol poop has not found in subscribes
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
    return await response_maker.crypto_remove_subscribe(session, request)


@router.route('/currency/make', methods=['POST'])
async def currency_make_subscribe():
    """
    Make currency subscribe
    ---
    tags:
        - SUBSCRIBE
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
                    message:
                        type: string
                        description: API message
                        example: Subscribe has made
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Subscribe has already made
        422:
            description: Invalid data sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Invalid symbol - poop
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
    return await response_maker.currency_make_subscribe(session, request)


@router.route('/currency/remove', methods=['DELETE'])
async def currency_remove_subscribe():
    """
    Remove currency subscribe
    ---
    tags:
        - SUBSCRIBE
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
                    message:
                        type: string
                        description: API message
                        example: Subscribe has removed
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: You do not have any subscribes
        422:
            description: Invalid data sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Symbol poop has not found in subscribes
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
    return await response_maker.currency_remove_subscribe(session, request)
