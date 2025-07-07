import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import handle_records, handle_start
from handlers.finance_db import FinanceDb

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
BASE_DIR = Path(__file__).resolve().parent


async def main():
    logging.info('Enter to main Bot')
    print("Bot has started")
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_routers(handle_start.router)
    dp.include_routers(handle_records.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler('log_main.log')
                  ],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    FinanceDb().create_db()
    asyncio.run(main())
