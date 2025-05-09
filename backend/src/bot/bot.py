from aiogram import Bot, Dispatcher

from src.config import settings
from .commands import commands
from .routers import base, register, special
from .middlewares.middleware import CreateConnDB


bot = Bot(
    token=settings.BOT_TOKEN
)

dp = Dispatcher()

dp.include_routers(
    base.router,
    register.router,
    special.router
)

dp.message.middleware(CreateConnDB())
dp.callback_query.middleware(CreateConnDB())


async def start_bot():
    await bot.set_my_commands(commands=commands)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
