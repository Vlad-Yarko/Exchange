import uuid

from flask import make_response, jsonify

from ..responses.response import Response
from ..utils.jwt import JWT
from src.databases.redis_client import redis_client


jwt_worker = JWT()


class SpamResponse(Response):
    @staticmethod
    async def spam(request):
        response = 'OK'
        headers = request.headers
        bearer_token = headers.get('Authorization')
        if bearer_token:
            username = jwt_worker.get_username(headers)
            if username:
                user_id = f'user-activity:{username}'
                last_url = await redis_client.get(f'user-url:{username}')
                current_url = request.url
                if last_url is None:
                    await redis_client.setex(f'user-url:{username}', 300, current_url)
                    return response
                if last_url == current_url:
                    user_activity = await redis_client.get(user_id)
                    if user_activity:
                        if int(user_activity) > 5:
                            response = make_response(jsonify(message='Suspicious activity detected'), 429)
                            return response
                    await redis_client.incr(user_id)
                    await redis_client.expire(user_id, 300)
                    return response
                else:
                    await redis_client.delete(f'user-url:{username}')
        return response
