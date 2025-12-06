# bot.py
import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("⚠️ Warning: BOT_TOKEN or CHAT_ID not set!")

bot = Bot(token=TOKEN) if TOKEN else None

async def send_message(message: str):
    if bot and CHAT_ID:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    else:
        print(f"[Bot disabled] Would send: {message}")
