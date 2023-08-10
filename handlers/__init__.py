from aiogram import Router
from middlewares.throttling import ThrottlingMiddleware
from utils.db_api import Database

router = Router()
router.message.middleware(ThrottlingMiddleware())
db = Database()

flags_default = {"throttling_key": "default"}
flags_request = {"throttling_key": "request"}

from . import commands
