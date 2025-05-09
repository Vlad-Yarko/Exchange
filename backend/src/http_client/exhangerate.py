from typing import Union

from aiohttp import ClientSession

from src.http_client.http_client import HTTPClient
from src.config import settings


class HTTPClientExchangeRate(HTTPClient):
    def __init__(self):
        super().__init__(
            base_url='https://api.exchangerate.host/'
        )

    async def get_symbol_price(self, symbol1, symbol2) -> Union[dict, bool]:
        self.endpoint = 'live'
        self.params = {
            'access_key': settings.EXCHANGE_API_KEY,
            'source': symbol1,
            'currencies': symbol2
        }
        async with ClientSession(base_url=self.base_url) as session:
            async with session.get(
                url=self.endpoint,
                params=self.params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    data = False
                    # data = response.json()
        return data
