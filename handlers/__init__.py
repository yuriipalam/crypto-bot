from aiogram import Router
from middleware.throttling import ThrottlingMiddleware
from utils.db_api import Database

router = Router()
router.message.middleware(ThrottlingMiddleware())
db = Database()

from . import default_commands
