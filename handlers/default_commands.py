import requests
from . import router, db
from datetime import datetime
from aiogram.filters import Command
from aiogram.types import Message
from const import ROOT


@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    answer = (
        "🤖 Hello, I am your Crypto Bot! 🚀\n\n"
        "I can provide you with the latest rates for BTC, ETH, SOL, and DOGE. Just type /rates to get the updates!\n\n"
        "📈 Additionally, I'll keep you informed when there are significant rate changes. Stay tuned for exciting news! 🎉"
    )

    db.add_user(message.from_user.id)

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
