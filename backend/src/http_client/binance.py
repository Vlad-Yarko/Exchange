from aiohttp import ClientSession

from ..http_client.http_client import HTTPClient


class HTTPClientBinance(HTTPClient):
    def __init__(self):
        super().__init__(
            base_url='https://api.binance.com/api/v3/'
        )

    async def get_symbol_price(self, symbol: str) -> dict:
        self.endpoint = 'ticker/price'
        self.params = {
            'symbol': symbol
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
        return data
