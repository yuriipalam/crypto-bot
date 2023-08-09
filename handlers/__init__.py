from aiogram import Router
from middleware.throttling import ThrottlingMiddleware

router = Router()
router.message.middleware(ThrottlingMiddleware())

from . import default_commands
