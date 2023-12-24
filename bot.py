import asyncio
import aioschedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.methods.send_message import SendMessage
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
import registration

async def scheduler(bot : Bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(registration.daily_horoscope, trigger='cron', args=[bot], hour=15, minute=49)
    scheduler.start()

async def on_startup(bot : Bot):
    asyncio.create_task(scheduler(bot))

async def main():
    bot = Bot('6500703441:AAHbFoGXeX--h3AQLWzJcclHCRDxI4ACgGA')
    dp = Dispatcher()
    dp.include_routers(registration.router)
    await on_startup(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

