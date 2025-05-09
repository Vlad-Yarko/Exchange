from ..utils.jwt import JWT


jwt_worker = JWT()


class Response:
    def __init__(self):
        pass

    @staticmethod
    def serialize_data(data):
        json_data = {}
        for row in data:
            json_data[row.id] = {
                'symbol': row.symbol,
                'symbol1': row.symbol1,
                'symbol2': row.symbol2
            }
        return json_data

    @staticmethod
    def get_username(request):
        bearer = jwt_worker.parse_bearer(request.headers.get('Authorization'))
        payload = jwt_worker.decode_token(bearer)
        username = payload.get('sub')
        return username
