import asyncio
import logging

from aiogram.types import BotCommand
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import router, dp, bot, current_coins_str
from middlewares import ThrottlingMiddleware
from schedulers import significant_rate_change


async def add_jobs(scheduler: BaseScheduler):
    scheduler.start()
    scheduler.add_job(significant_rate_change, 'interval', hours=4)


async def set_bot_parameters():  # set parameters that change dynamically
    await bot.set_my_description(
        f"Stay ahead of the crypto curve with Crypto Notifier! Get real-time rates for {current_coins_str} and receive alerts "
        f"on major changes. Your ultimate crypto companion. 🚀📈"
    )
    await bot.set_my_commands(
        [
            BotCommand(command="help", description="Need assistance? 🆘"),
            BotCommand(command="rates", description=f"Current rates for {current_coins_str} 📊💰"),
            BotCommand(command="rate_changes", description="Monitor rate changes compared to yesterday 🔄")
        ]
    )


async def main() -> None:
    await set_bot_parameters()

    router.message.middleware(ThrottlingMiddleware())
    import handlers

    await significant_rate_change()
    dp.include_router(router)
    dp.startup.register(add_jobs)
    await dp.start_polling(bot, scheduler=AsyncIOScheduler())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
