from aiogram import Dispatcher, Bot, Router
from aiogram.enums import ParseMode

from const import BOT_TOKEN
from utils.db_api import Database

dp = Dispatcher()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

router = Router()

db = Database()
