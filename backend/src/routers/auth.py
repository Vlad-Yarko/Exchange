from flask import Blueprint

from ..responses.auth_response import AuthResponse


router = Blueprint('auth', __name__)
response_maker = AuthResponse()


@router.route('/signup', methods=['POST'])
async def signup_hand():
    """
        Register account
    ---
    tags:
        - AUTH
    consumes:
        - multipart/form-data
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: Username to register
      - name: password
        in: formData
        type: string
        required: true
        description: Password to register
      - name: email
        in: formData
        type: string
        required: true
        description: Email to register
    responses:
        200:
            description: Correct credentials
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: API message
                        example: Good credentials, email was sent
        422:
            description: Invalid credentials
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: error message
                        example: Password is invalid
    """
    return await response_maker.signup_hand_response()


@router.route('/login', methods=['POST'])
async def login_hand():
    """
        Authenticate
    ---
    tags:
        - AUTH
    consumes:
        - multipart/form-data
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: Username to authenticate
      - name: password
        in: formData
        type: string
        required: true
        description: Password to authenticate
    responses:
        200:
            description: Correct credentials
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: API message
                        example: Good credentials, refresh token is created
        403:
            description: Refresh token is already exist
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Refresh token has already found
        422:
            description: Invalid credentials
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: error message
                        example: Password is invalid
    """
    return await response_maker.login_hand_response()


@router.route('/logout', methods=['POST'])
async def logout_hand():
    """
            Log out
        ---
        tags:
            - AUTH
        consumes:
            - application/json
        responses:
            200:
                description: Correct credentials
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: API message
                            example: Refresh token was deleted
            401:
                description: Refresh token is already expired or missing
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: API message
                            example: Refresh token was expired
        """
    return await response_maker.logout_hand_response()


@router.route('/refresh', methods=['POST'])
async def refresh_hand():
    """
    Refresh access token
    ---
    tags:
        - AUTH
    consumes:
        - application/json
    responses:
        200:
            description: Refresh token is valid
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: API message
                        example: Refresh token is valid
                    bearerToken:
                        type: string
                        description: Bearer token
                        example: afdhaskljfhajklfjkafhjlajkf
        401:
            description: Refresh token missing
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Refresh token is missing
        403:
            description: Refresh token expired
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Refresh token is expired
    """
    return await response_maker.refresh_hand_response()


@router.route('/verify-mail', methods=['POST'])
async def verify_mail_hand():
    """
        Send message on a given email
        ---
        tags:
            - AUTH
        consumes:
            - multipart/form-data
        parameters:
        - name: code
          in: formData
          type: number
          required: true
          description: The code that was sent on entered email address
        responses:
            200:
                description: Correct email code
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: API message
                            example: Good
            403:
                description: Server conflict
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error API message
                            example: Time to sign up has already passed
            422:
                description: Giver email code is invalid
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error API message
                            example: Invalid code
    """
    return await response_maker.verify_mail_hand_response()


@router.route('/login/google', methods=['GET'])
async def google_login_hand():
    """
    Send message on a given email
    ---
    tags:
        - AUTH
    consumes:
        - multipart/form-data
    responses:
        302:
            description: Everything is good
            headers:
                Location:
                    type: string
                    description: The google url authorization url
                    example: /auth/authorize/google
        403:
            description: Server conflict
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: You are already logged in
        """
    return await response_maker.google_login_hand_response()


@router.route('/authorize/google', methods=['GET'])
async def google_authorize_hand():
    """
        Send message on a given email
        ---
        tags:
            - AUTH
        consumes:
            - multipart/form-data
        responses:
            200:
                description: Correct authorization
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: API message
                            example: Good
            403:
                description: Server conflict
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error API message
                            example: You are already logged in
    """
    return await response_maker.google_authorize_hand_response()
