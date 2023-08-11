from const import ROOT


def currency_prices_usd(ids):
    return ROOT + f"/simple/price?ids={ids}&vs_currencies=usd"


def rate_range(coin_id, from_stamp, to_stamp):
    return ROOT + f"/coins/{coin_id}/market_chart/range?vs_currency=usd&from={from_stamp}&to={to_stamp}"
