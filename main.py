import asyncio
import logging

from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import router, dp, bot
from middlewares.throttling import ThrottlingMiddleware
from schedulers.significant_rate_change import significant_rate_change


async def add_jobs(scheduler: BaseScheduler):
    scheduler.start()
    scheduler.add_job(significant_rate_change, 'interval', minutes=20)


async def main() -> None:
    router.message.middleware(ThrottlingMiddleware())
    import handlers

    dp.include_router(router)
    dp.startup.register(add_jobs)
    await dp.start_polling(bot, scheduler=AsyncIOScheduler())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
