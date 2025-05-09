from flask import Blueprint, request, g

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
        example: mister_business
      - name: password
        in: formData
        type: string
        required: true
        description: Password to register
        example: 12345678
      - name: email
        in: formData
        type: string
        required: true
        description: Email to register
        example: mister_business@gmail.com
    responses:
        200:
            description: Good request
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: API message
                        example: Correct credentials
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Refresh token has already found
        422:
            description: Invalid data was sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: error message
                        example: Password is invalid
    """
    return await response_maker.signup_hand(request)


@router.route('/verify-mail', methods=['POST'])
async def verify_mail_hand():
    """
    Entered sent code on email
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
      description: Six-digit code that was sent on entered email address
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
                        example: Correct credentials
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Time to sign up has already passed
        422:
            description: Invalid data sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Entered code is invalid
    """
    session = g.session
    return await response_maker.verify_mail_hand(session, request)


@router.route('/login/username', methods=['POST'])
async def login_username_hand():
    """
    Log in by username
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
        description: Username to log in
        example: mister_business
      - name: password
        in: formData
        type: string
        required: true
        description: Password to log in
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
                        example: Good credentials
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Refresh token has already found
        422:
            description: Invalid data was sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: error message
                        example: Password is invalid
    """
    return await response_maker.login_username_hand(request)


@router.route('/login/email', methods=['POST'])
async def login_email_hand():
    """
    Log in by email
    ---
    tags:
        - AUTH
    consumes:
        - multipart/form-data
    parameters:
      - name: email
        in: formData
        type: string
        required: true
        description: Email to log in
        example: mister_business@gmail.com
      - name: password
        in: formData
        type: string
        required: true
        description: Password to log in
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
                        example: Good credentials
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Refresh token has already found
        422:
            description: Invalid data was sent
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: error message
                        example: Password is invalid
    """
    return await response_maker.login_email_hand(request)


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
            description: Good request
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: API message
                        example: Refresh token has deleted
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: API message
                        example: Refresh token has expired
    """
    return await response_maker.logout_hand(request)


@router.route('/refresh', methods=['POST'])
async def refresh_hand():
    """
    Create new access token
    ---
    tags:
        - AUTH
    consumes:
        - application/json
    responses:
        200:
            description: Good request
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
        403:
            description: Access denied
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Refresh token has expired
    """
    return await response_maker.refresh_hand(request)


# Need to be replaced with POST method
@router.route('/login/google', methods=['GET'])
async def google_login_hand():
    """
    Google log in
    ---
    tags:
        - AUTH
    # consumes:
    #     - multipart/form-data
    # responses:
    #     302:
    #         description: Everything is good
    #         headers:
    #             Location:
    #                 type: # string
    #                 description: The Google url authorization url
    #                 example: /auth/authorize/google
    #     403:
    #         description: Server conflict
    #         schema:
    #             type: # object
    #             properties:
    #                 message:
    #                     type: # string
    #                     description: Error API message
    #                     example: You are already logged in
    # """
    return await response_maker.google_login_hand(request)


# Need to be replaced with POST method
@router.route('/authorize/google', methods=['GET'])
async def google_authorize_hand():
    """
    Google log in
    ---
    tags:
        - AUTH
    # consumes:
    #     - multipart/form-data
    # responses:
    #     200:
    #         description: Correct authorization
    #         schema:
    #             type: # object
    #             properties:
    #                 message:
    #                     type: # string
    #                     description: API message
    #                     example: Good
    #     403:
    #         description: Server conflict
    #         schema:
    #             type: # object
    #             properties:
    #                 message:
    #                     type: # string
    #                     description: Error API message
    #                     example: You are already logged in
    """
    session = g.session
    return await response_maker.google_authorize_hand(session, request)


@router.route('/is-logged-in', methods=['POST'])
async def is_logged_in_hand():
    """
    Is logged in user
    ---
    tags:
        - AUTH
    consumes:
        - application/json
    responses:
        200:
            description: Good request
            schema:
                type: object
                properties:
                    message:
                        type: boolean
                        description: API message ( true or false )
                        example: true
    """
    return await response_maker.is_logged_in_hand(request)
