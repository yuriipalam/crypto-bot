import requests

from const import ROOT
from loader import bot, db
from datetime import datetime, timedelta


async def significant_rate_change():
    current_time = datetime.now()
    two_hours_ago = current_time - timedelta(hours=2)
    current_timestamp = current_time.timestamp()
    two_hours_ago_timestamp = two_hours_ago.timestamp()

    coins = db.select_all_coins()

    for coin in coins:
        if coin[6] == 1:
            url = ROOT + f"/coins/{coin[1]}/market_chart/range?vs_currency=usd&from={two_hours_ago_timestamp}&to={current_timestamp}"
            resp = requests.request("GET", url).json()
            prices = resp['prices']

            curren_price = prices[-1][1]
            two_hours_ago_price = prices[0][1]
            diff = curren_price - two_hours_ago_price

            direction = "⬆️ increased" if diff > 0 else "⬇️ decreased"

            if coin[5] * -1 >= diff or diff >= coin[5]:
                users = db.select_all_users()
                for user in users:
                    message = (
                        f"⚠️ Alert! {coin[2]} rate has {direction} significantly within the last 2 hours! ⚠️\n\n"
                        f"Previous rate: {two_hours_ago_price:.{coin[3]}f} USD\n"
                        f"New rate: {curren_price:.{coin[3]}f} USD\n"
                        f"Difference: {diff:.{coin[3]}f} USD\n\n"
                        "Stay tuned for more updates! 🚀📈"
                    )

                    await bot.send_message(user[0], message)
