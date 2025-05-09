import asyncio

from src.api.api import start_api
from src.bot.bot import start_bot
from src.scheduler.scheduler import start_scheduler


async def main():
    await asyncio.gather(
        start_api(),
        start_bot(),
        start_scheduler()
    )


if __name__ == '__main__':
    asyncio.run(main())
