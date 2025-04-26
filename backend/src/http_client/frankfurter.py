from aiohttp import ClientSession

from ..http_client.http_client import HTTPClient
from ..config import settings


class HTTPClientFrankFurter(HTTPClient):
    def __init__(self):
        super().__init__(
            base_url='https://api.frankfurter.dev/v1/'
        )

    async def get_symbol_price(self, symbol1, symbol2) -> dict:
        self.endpoint = 'latest'
        self.params = {
            'base': symbol1,
            'symbols': symbol2
        }
        async with ClientSession(base_url=self.base_url) as session:
            async with session.get(
                url=self.endpoint,
                params=self.params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    # data = False
                    data = await response.json()
        return data


import asyncio
cl = HTTPClientFrankFurter()
data = asyncio.run(cl.get_symbol_price('USD', 'UAH'))
print(data)
