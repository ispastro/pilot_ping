import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scrapper import main


scheduler = AsyncIOScheduler()


scheduler.add_job(main, 'cron', day_of_week ="sun,mon, wed,fri", hour=9 , minute=0)
scheduler.start()

print("🛰 Scheduler started. Waiting for the next mission...")

asyncio.get_event_loop().run_forever()