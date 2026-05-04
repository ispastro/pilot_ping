import asyncio
import requests
from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from lib.db import is_new_job, get_subscribers
from lib.bot import broadcast

URL = "https://corporate.ethiopianairlines.com/AboutEthiopian/careers/vacancies/2"


async def scrape_and_notify():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))

    try:
        response = session.get(URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return

    soup = BeautifulSoup(response.text, "html.parser")
    jobs_found = []

    for job in soup.find_all("a"):
        text = job.get_text(strip=True)
        text_lower = text.lower()
        if "pilot" in text_lower and "trainee" in text_lower:
            link = urljoin(URL, job.get("href", ""))
            if is_new_job(text, link):
                jobs_found.append((text, link))

    if jobs_found:
        subscribers = get_subscribers()
        if subscribers:
            messages = [f"📋 *{text}*\n🔗 [Apply Here]({link})" for text, link in jobs_found]
            message = f"🚀 *{len(jobs_found)} New Pilot Job(s) Found!*\n\n" + "\n\n".join(messages)
            await broadcast(message, subscribers)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        asyncio.run(scrape_and_notify())
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"done")

    def log_message(self, format, *args):
        pass
