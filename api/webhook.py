import asyncio
import json
from http.server import BaseHTTPRequestHandler
from lib.db import add_subscriber, remove_subscriber, is_subscriber
from lib.bot import send_message


def handle_update(update: dict):
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if not chat_id:
        return

    if text == "/start":
        add_subscriber(chat_id)
        asyncio.run(send_message(chat_id, "✅ *Subscribed!* You'll be notified when new pilot jobs drop on Ethiopian Airlines."))
    elif text == "/stop":
        remove_subscriber(chat_id)
        asyncio.run(send_message(chat_id, "🛑 *Unsubscribed.* You won't receive any more alerts."))
    elif text == "/status":
        if is_subscriber(chat_id):
            asyncio.run(send_message(chat_id, "✅ You are *subscribed* and will receive job alerts."))
        else:
            asyncio.run(send_message(chat_id, "❌ You are *not subscribed*. Send /start to subscribe."))


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        handle_update(body)
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        pass
