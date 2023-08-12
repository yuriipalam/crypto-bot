from aiogram import Dispatcher, Bot, Router
from aiogram.enums import ParseMode

from const import BOT_TOKEN
from utils import Database
from utils import RequestsAPI

dp = Dispatcher()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

router = Router()

db = Database()

coin_abbs = [x[2] for x in db.select_all_coins()]
current_coins_str = f"{', '.join([x for x in coin_abbs[0:-1]])}, and {coin_abbs[-1]}"

requests_api = RequestsAPI()
