from dotenv import dotenv_values

config = dotenv_values(".env")

BOT_TOKEN = config["BOT_TOKEN"]
ROOT = "https://api.coingecko.com/api/v3"  # open api, no auth

HOURS_TO_UPDATE = 5
