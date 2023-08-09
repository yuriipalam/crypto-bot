import asyncio
import logging

from const import BOT_TOKEN
from handlers import router
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
