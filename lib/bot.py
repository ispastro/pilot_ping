import os
import httpx

TOKEN = os.environ["BOT_TOKEN"]
BASE = f"https://api.telegram.org/bot{TOKEN}"

async def send_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE}/sendMessage", json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        })

async def broadcast(text: str, chat_ids: list[int]):
    async with httpx.AsyncClient() as client:
        for chat_id in chat_ids:
            await client.post(f"{BASE}/sendMessage", json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown"
            })
