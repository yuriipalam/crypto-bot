import asyncio
import logging
import requests

from datetime import datetime
from aiogram import Bot, Dispatcher, Router
from dotenv import dotenv_values

from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

config = dotenv_values(".env")

BOT_TOKEN = config["BOT_TOKEN"]
ROOT = "https://api.coingecko.com/api/v3"  # open api, no auth

router = Router()


@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    answer = (
        "🤖 Hello, I am your Crypto Bot! 🚀\n\n"
        "I can provide you with the latest rates for BTC, ETH, SOL, and DOGE. Just type /rates to get the updates!\n\n"
        "📈 Additionally, I'll keep you informed when there are significant rate changes. Stay tuned for exciting news! 🎉"
    )

    await message.answer(answer)


@router.message(Command("rates"))
async def command_rates_handler(message: Message) -> None:
    url = ROOT + "/simple/price?ids=bitcoin,ethereum,solana,dogecoin&vs_currencies=usd"
    resp = requests.request("GET", url).json()

    time = datetime.now().strftime("%H:%M:%S, %d/%m/%Y")

    answer = (
        f"🕒 Crypto rates at {time} GMT 🕒\n\n"
        f"💰 BTC: {resp['bitcoin']['usd']:.2f} USD\n"
        f"💎 ETH: {resp['ethereum']['usd']:.2f} USD\n"
        f"☀️ SOL: {resp['solana']['usd']:.2f} USD\n"
        f"🐶 DOGE: {resp['dogecoin']['usd']:.6f} USD\n"
    )

    await message.answer(answer)


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
