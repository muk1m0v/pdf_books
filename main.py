import asyncio
from os import getenv
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from color.style import *
from handlers.route import router
from database.db import init_tables

load_dotenv()
bot = Bot(token=getenv('BOT_TOKEN'))

dp = Dispatcher()

async def main():
    print(lblue + 'Bot working ■■■■■■■■■■■■■■■■ 100%' + reset)

    init_tables()
    await dp.include_router(router=router)

if __name__ == '__main__':
    asyncio.run(main())