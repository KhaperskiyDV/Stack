import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType
from core.handlers.basic import *
from core.settings import settings
from aiogram.filters import Command

async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot started!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot stoped!')


async def start():
    logging.basicConfig(level=logging.INFO, 
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    bot = Bot(token=settings.bots.bot_token)

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.include_router(user_private_router)
    

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__== "__main__":
    asyncio.run(start())