import asyncio
from datetime import datetime, date

from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, ErrorEvent

from keyboards import main_keyboard
from keyboards.main import rates_button, help_button, rate_changes_button
from loader import db, router, requests_api, current_coins_str
from . import flags_default, flags_request


@router.message(Command("start"), flags=flags_default)
async def command_start_handler(message: Message) -> None:
    answer = (
        "🤖 Hello, I am your Crypto Bot! 🚀\n\n"
        f"I can provide you with the latest rates for {current_coins_str}. Just type /rates to get the updates!\n\n"
        "Also, use the /rate_changes command to receive updates on how the rates have changed ⬆️⬇️ compared to the previous day.\n\n"
        "🆘 List of available commands: /help\n\n"
        "📈 Additionally, I'll keep you informed when there are significant rate changes. Stay tuned for exciting news! 🎉"
    )

    db.add_user(message.from_user.id)

    await message.answer(answer, reply_markup=main_keyboard)


@router.message(F.text == help_button.text, flags=flags_default)
@router.message(Command("help"), flags=flags_default)
async def command_help_handler(message: Message) -> None:
    answer = (
        "🤖 Welcome to Crypto Bot! 🚀\n\n"
        "Stay updated with the latest cryptocurrency rates and receive alerts on significant rate changes.Let's explore the exciting world of cryptocurrencies together!\n\n"
        "/help - Need Assistance? 🆘\n"
        "Seek guidance on interacting with Crypto Bot's features and commands.\n\n"
        "/rates - Check Current Rates 📈\n"
        "Obtain the latest rates of selected cryptocurrencies against USD. Stay informed about the ever-changing crypto market.\n\n"
        "/rate_changes - Monitor Rate Changes 📊\n"
        "Receive updates on how rates have changed compared to the previous day. Stay aware of upward, downward, and stagnant trends.\n\n"
    )

    await message.reply(answer, reply_markup=main_keyboard)


@router.message(F.text == rates_button.text, flags=flags_request)
@router.message(Command("rates"), flags=flags_request)
async def command_rates_handler(message: Message) -> None:
    msg_working = await message.answer("Working on it... 👨‍💻")

    coins = db.select_all_coins()

    resp = await requests_api.get_currency_prices_usd([coin[1] for coin in coins], msg_working=msg_working)

    time = datetime.now().strftime("%H:%M:%S, %d/%m/%Y")

    coins_answer = "\n".join([f"{coin[4]} {coin[2]}: {resp[coin[1]]['usd']:.{coin[3]}f} USD" for coin in coins])
    answer = f"🕒 Crypto rates at {time} GMT\n\n" + coins_answer

    await msg_working.delete()

    await message.answer(answer, reply_markup=main_keyboard)


@router.message(F.text == rate_changes_button.text, flags=flags_request)
@router.message(Command("rate_changes"), flags=flags_request)
async def command_rate_changes_handler(message: Message) -> None:
    msg_working = await message.answer("Working on it... 👨‍💻")

    coins = db.select_all_coins()

    current_time_stamp = datetime.now().timestamp()
    start_of_day_stamp = datetime.combine(date.today(), datetime.min.time()).timestamp()

    coins_answer = []

    for coin in coins:
        resp = await requests_api.get_rate_range(coin[1], start_of_day_stamp, current_time_stamp,
                                                 msg_working=msg_working)

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
    answer = f"🕒 Rate changes at {time} GMT, Compared to yesterday\n\n" + "\n\n".join(coins_answer)

    await message.answer(answer, reply_markup=main_keyboard)


@router.message(flags=flags_default)
async def any_message_handler(message: Message):
    await message.answer("Can't help you with that, see /help to know what I can do 😉", reply_markup=main_keyboard)


@router.error()
async def error_handler(event: ErrorEvent):
    await event.update.message.answer("Something went wrong... Try again, please 😕", reply_markup=main_keyboard)
