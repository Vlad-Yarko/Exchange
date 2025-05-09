import asyncio

from src.http_client.api_client import HTTPClientAPI


http_worker = HTTPClientAPI()


async def start_scheduler():
    while True:
        await http_worker.alert_all()
        await asyncio.sleep(300)
