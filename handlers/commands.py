import requests
from . import flags_default, flags_request
from datetime import datetime
from aiogram.filters import Command
from aiogram.types import Message
from const import ROOT
from loader import db, router


@router.message(Command("start"), flags=flags_default)
async def command_start_handler(message: Message) -> None:
    answer = (
        "🤖 Hello, I am your Crypto Bot! 🚀\n\n"
        "I can provide you with the latest rates for BTC, ETH, SOL, and DOGE. Just type /rates to get the updates!\n\n"
        "📈 Additionally, I'll keep you informed when there are significant rate changes. Stay tuned for exciting news! 🎉"
    )

    db.add_user(message.from_user.id)

    await message.answer(answer)


@router.message(Command("rates"), flags=flags_request)
async def command_rates_handler(message: Message) -> None:
    coins = db.select_all_coins()
    ids = ",".join([coin[1] for coin in coins])

    url = ROOT + f"/simple/price?ids={ids}&vs_currencies=usd"
    resp = requests.request("GET", url).json()

    time = datetime.now().strftime("%H:%M:%S, %d/%m/%Y")

    coins_answer = "\n".join([f"{coin[4]} {coin[2]} {resp[coin[1]]['usd']:.{coin[3]}f} USD" for coin in coins])
    answer = f"🕒 Crypto rates at {time} GMT 🕒\n\n" + coins_answer

    await message.answer(answer)
