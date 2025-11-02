import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

async def main():
    updates = await bot.get_updates()
    for u in updates:
        print(u.message.chat.id, u.message.chat.first_name)

asyncio.run(main())
