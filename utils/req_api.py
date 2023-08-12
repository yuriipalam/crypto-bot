import asyncio

import requests
from aiogram.types import Message

from const import ROOT


class RequestsAPI:
    async def _get_request(self, url, msg_working: Message = None):
        async def wrapper(*args, **kwargs):
            resp = requests.request("GET", url).json()
            if "status" in resp:
                if resp["status"]["error_code"] == 429:
                    if msg_working is not None:
                        await asyncio.sleep(2)
                        await msg_working.edit_text(
                            "Working on it... 👨‍💻 Processing time is longer than usual due to server load, sorry for the inconvience 🤕")
                    await asyncio.sleep(60)
                    return await wrapper(*args, **kwargs)
                raise requests.RequestException
            return resp

        return await wrapper()

    def _currency_prices_usd_url(self, coin_ids):
        return ROOT + f"/simple/price?ids={','.join([x for x in coin_ids])}&vs_currencies=usd"

    async def get_currency_prices_usd(self, coin_ids, msg_working: Message = None):
        return await self._get_request(self._currency_prices_usd_url(coin_ids), msg_working=msg_working)

    def _rate_range_url(self, coin_id, from_stamp, to_stamp):
        return ROOT + f"/coins/{coin_id}/market_chart/range?vs_currency=usd&from={from_stamp}&to={to_stamp}"

    async def get_rate_range(self, coin_id, from_stamp, to_stamp, msg_working: Message = None):
        return await self._get_request(self._rate_range_url(coin_id, from_stamp, to_stamp), msg_working=msg_working)
