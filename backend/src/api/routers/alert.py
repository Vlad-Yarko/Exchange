from flask import Blueprint, request, g

from ..responses.alert_response import AlertResponse


router = Blueprint('alert', __name__)
response_maker = AlertResponse()


@router.route('/all', methods=['POST'])
async def alert_all_hand():
    # Need to add some protection
    """
    Alert all subscribed users
    ---
    tags:
        - ALERT
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
                        example: Subscribed users were alerted
        422:
            description: Bad request
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error API message
                        example: Crypto subscribes are empty
    """
    session = g.session
    return await response_maker.alert_all_hand(session)
