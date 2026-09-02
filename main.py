import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import load_settings
from handlers import routers


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    settings = load_settings()
    bot = Bot(token=settings.bot_token)
    dispatcher = Dispatcher()

    for router in routers:
        dispatcher.include_router(router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
