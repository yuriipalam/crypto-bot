from aiogram import Dispatcher, Bot, Router
from aiogram.enums import ParseMode

from const import BOT_TOKEN
from utils import Database
from utils import RequestsAPI

dp = Dispatcher()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

router = Router()

db = Database()
requests_api = RequestsAPI()
