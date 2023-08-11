import asyncio

import requests

from utils import api_urls
from . import flags_default, flags_request
from datetime import datetime, timedelta, date
from aiogram.filters import Command
from aiogram.types import Message
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


@router.message(Command("help"), flags=flags_default)
async def command_help_handler(message: Message) -> None:
    answer = (
        "🤖 Welcome to Crypto Bot! 🚀\n\n"
        "Stay updated with the latest cryptocurrency rates and receive alerts on significant rate changes.Let's explore the exciting world of cryptocurrencies together!\n\n"
        "/help - Need Assistance? 🆘\n"
        "Seek guidance on interacting with Crypto Bot's features and commands.\n\n"
        "/rates - Check Current Rates 📈\n"
        "Obtain the latest rates of selected cryptocurrencies against USD. Stay informed about the ever-changing crypto market.\n\n"
        "/rate_changes - Monitor Rate Changes 🔄\n"
        "Receive updates on how rates have changed compared to the previous day. Stay aware of upward, downward, and stagnant trends.\n\n"
    )

    await message.reply(answer)


@router.message(Command("rates"), flags=flags_request)
async def command_rates_handler(message: Message) -> None:
    coins = db.select_all_coins()

    ids = ",".join([coin[1] for coin in coins])
    url = api_urls.currency_prices_usd(ids)
    resp = requests.request("GET", url).json()

    time = datetime.now().strftime("%H:%M:%S, %d/%m/%Y")

    coins_answer = "\n".join([f"{coin[4]} {coin[2]}: {resp[coin[1]]['usd']:.{coin[3]}f} USD" for coin in coins])
    answer = f"🕒 Crypto rates at {time} GMT 🕒\n\n" + coins_answer

    await message.answer(answer)


@router.message(Command("rate_changes"), flags=flags_request)
async def command_rate_changes_handler(message: Message) -> None:
    msg_working = await message.answer("Working on it... 👨‍💻")

    coins = db.select_all_coins()

    current_time_stamp = datetime.now().timestamp()
    start_of_day_stamp = datetime.combine(date.today(), datetime.min.time()).timestamp()

    coins_answer = []

    for coin in coins:
        url = api_urls.rate_range(coin[1], start_of_day_stamp, current_time_stamp)
        resp = requests.request("GET", url).json()

        prices = resp["prices"]
        current_price = prices[-1][1]
        start_of_day_price = prices[0][1]
        percentage = (100 * current_price / start_of_day_price) - 100

        if percentage > 0:
            direction = "⬆️ increased"
        elif percentage < 0:
            direction = "⬇️ decreased"
        else:
            direction = "🔁 stagnated"

        coins_answer.append(
            f"{coin[4]} {coin[2]}: {current_price:.{coin[3]}f} USD\n{direction} {f'by {percentage:.3f}%' if percentage != 0 else ''} from {start_of_day_price:.{coin[3]}f} USD")

        await asyncio.sleep(2)

    await msg_working.delete()

    time = datetime.now().strftime("%H:%M:%S, %d/%m/%Y")
    answer = f"🕒 Rate changes at {time} GMT, Compared to yesterday 🕒\n\n" + "\n\n".join(coins_answer)

    await message.answer(answer)
