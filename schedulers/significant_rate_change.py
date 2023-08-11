import asyncio

import requests

from loader import bot, db
from datetime import datetime, timedelta, date

from utils import api_urls


def calculate_diff_to_compare(coin):
    start_of_day = datetime.combine(date.today(), datetime.min.time())
    day_ago_stamp = (start_of_day - timedelta(days=1)).timestamp()

    url = api_urls.rate_range(coin[1], day_ago_stamp, start_of_day.timestamp())
    resp = requests.request("GET", url).json()

    prices = [x[1] for x in resp['prices']]

    return abs(max(prices) - min(prices))


async def significant_rate_change():
    current_time_stamp = datetime.now().timestamp()
    start_of_day_stamp = datetime.combine(date.today(), datetime.min.time()).timestamp()

    coins = db.select_all_coins()

    for coin in coins:
        if coin[5] == 1:
            url = api_urls.rate_range(coin[1], start_of_day_stamp, current_time_stamp)
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
