import logging

from aiogram import Bot, Dispatcher

from bot.handlers.handlers import router
from core import settings


async def start_bot():
    """Bot entry point"""
    mybot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(router)

    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(mybot)
