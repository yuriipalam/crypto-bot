import asyncio

import requests

from const import ROOT
from loader import bot, db
from datetime import datetime, timedelta


def calculate_diff_to_compare(coin):
    current_time = datetime.now()
    day_ago_stamp = (current_time - timedelta(days=1)).timestamp()
    one_week_ago_stamp = (current_time - timedelta(days=2)).timestamp()

    url = ROOT + f"/coins/{coin[1]}/market_chart/range?vs_currency=usd&from={one_week_ago_stamp}&to={day_ago_stamp}"
    resp = requests.request("GET", url).json()

    prices = [x[1] for x in resp['prices']]

    return abs(max(prices) - min(prices))


async def significant_rate_change():
    current_time = datetime.now()
    time_ago = current_time - timedelta(hours=8)
    current_timestamp = current_time.timestamp()
    time_ago_timestamp = time_ago.timestamp()

    coins = db.select_all_coins()

    for coin in coins:
        if coin[5] == 1:
            url = ROOT + f"/coins/{coin[1]}/market_chart/range?vs_currency=usd&from={time_ago_timestamp}&to={current_timestamp}"
            resp = requests.request("GET", url).json()
            prices = resp['prices']  # list of pairs (timestamp, price)

            prices_only = [x[1] for x in prices]  # list of only prices [price,...]
            min_price = min(prices_only)
            max_price = max(prices_only)
            curren_price = prices[-1][1]

            compare_diff = calculate_diff_to_compare(coin)

            if (curren_price - min_price) >= compare_diff:
                time_ago_price = min_price
                diff = abs(curren_price - min_price)
                direction = "⬆️ increased"
            elif abs(curren_price - max_price) >= compare_diff:
                time_ago_price = max_price
                diff = curren_price - max_price
                direction = "⬇️ decreased"
            else:
                break

            users = db.select_all_users()
            for user in users:
                message = (
                    f"⚠️ Alert! {coin[2]} rate has {direction} significantly within the last time! ⚠️\n\n"
                    f"Previous rate: {time_ago_price:.{coin[3]}f} USD\n"
                    f"New rate: {curren_price:.{coin[3]}f} USD\n"
                    f"Difference: {diff:.{coin[3]}f} USD\n\n"
                    "Stay tuned for more updates! 🚀📈"
                )

                await bot.send_message(user[0], message)

        await asyncio.sleep(7)
