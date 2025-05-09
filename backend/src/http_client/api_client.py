from aiohttp import ClientSession

from src.http_client.http_client import HTTPClient


class HTTPClientAPI(HTTPClient):
    def __init__(self):
        super().__init__(
            base_url='http://127.0.0.1:8000/'
        )

    async def alert_all(self) -> None:
        self.endpoint = 'alert/all'
        async with ClientSession(base_url=self.base_url) as session:
            await session.post(url=self.endpoint)
