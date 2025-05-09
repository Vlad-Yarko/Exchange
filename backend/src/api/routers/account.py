from flask import Blueprint, request, g
from flask_cors import cross_origin

from ..responses.account_response import AccountResponse, jwt_worker


router = Blueprint('account', __name__)
response_maker = AccountResponse()


@router.before_request
async def account_before_request_hand():
    response = await jwt_worker.validate_bearer(g.session, request)
    if response != 'OK':
        return response


@router.route('/send/email', methods=['POST'])
async def send_account_email_hand():
    """
    Send email code
    ---
    tags:
        - ACCOUNT
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
                    message:
                        type: string
                        description: API message
                        example: Email was sent
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
    return await response_maker.send_account_email_hand(session, request)


@router.route('/verify/email', methods=['POST'])
async def validate_account_email_hand():
    """
    Verify email code
    ---
    tags:
        - ACCOUNT
    consumes:
        - multipart/form-data
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
        example: Bearer fajdfkjdsfkjldfdkdkgfhjwgh
      - name: code
        in: formData
        type: number
        required: true
        description: Six-digit code that was sent on email address
        example: 123456
    responses:
        200:
            description: Good request
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: API message
                        example: Entered code was correct
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Time to validate has already passed
        422:
            description: Invalid data was sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Entered code is invalid
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
    return await response_maker.validate_account_email_hand(request)


@router.route('/change/username', methods=['PUT'])
async def change_account_username_hand():
    """
    Change username
    ---
    tags:
        - ACCOUNT
    consumes:
      - multipart/form-data
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
        example: Bearer fajdfkjdsfkjldfdkdkgfhjwgh
      - name: username
        in: formData
        type: string
        required: true
        description: New username to change
        example: mister_business
    responses:
        200:
            description: Good request
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: API message
                        example: Username has changed
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
            description: Invalid data sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Username is already taken
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
    return await response_maker.change_account_username_hand(session, request)


@router.route('/change/password', methods=['PUT'])
async def change_account_password_hand():
    """
    Change password
    ---
    tags:
        - ACCOUNT
    consumes:
      - multipart/form-data
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
        example: Bearer fajdfkjdsfkjldfdkdkgfhjwgh
      - name: password
        in: formData
        type: string
        required: true
        description: New password to change
        example: 12345678
    responses:
        200:
            description: Good request
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: API message
                        example: Password has changed
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
            description: Invalid data sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Invalid password was sent
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
    return await response_maker.change_account_password_hand(session, request)


@router.route('/send/phone-number', methods=['POST'])
async def send_phone_number_hand():
    """
    Send code on phone number via telegram
    ---
    tags:
        - ACCOUNT
    consumes:
      - multipart/form-data
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
        example: Bearer fajdfkjdsfkjldfdkdkgfhjwgh
      - name: phoneNumber
        in: formData
        type: string
        required: true
        description: New phone number to change
        example: +380999999999
    responses:
        200:
            description: Good request
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: API message
                        example: Code was sent via telegram
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
            description: Invalid data sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Entered invalid phone number
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
    return await response_maker.send_phone_number_hand(session, request)


@router.route('/verify/phone-number', methods=['PUT'])
async def verify_new_phone_number_hand():
    """
    Verify new phone number
    ---
    tags:
        - ACCOUNT
    consumes:
      - multipart/form-data
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token - Bearer
        example: Bearer fajdfkjdsfkjldfdkdkgfhjwgh
      - name: code
        in: formData
        type: number
        required: true
        description: Six-digit code that was sent via telegram
        example: 123456
    responses:
        200:
            description: Good request
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: API message
                        example: Phone number has been changed
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
            description: Invalid data sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Invalid code sent
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
    return await response_maker.verify_new_phone_number_hand(session, request)


@router.route('/remove/phone-number', methods=['DELETE'])
async def remove_account_phone_number_hand():
    """
    Remove account phone number
    ---
    tags:
        - ACCOUNT
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
                    message:
                        type: string
                        description: API message
                        example: Phone number has removed
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Phone number has not found
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
    return await response_maker.remove_account_phone_number_hand(session, request)


@router.route('/info', methods=['GET', 'OPTIONS'])
# @cross_origin(supports_credentials=True)
async def account_info_hand():
    """
    Get user info
    ---
    tags:
        - ACCOUNT
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
                    username:
                        type: string
                        description: User username
                        example: mister_business
                    email:
                        type: string
                        description: User email
                        example: mister_business@gmail.com
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
    return await response_maker.account_info_hand(session, request)
