import asyncio
import requests
import sqlite3
from bs4 import BeautifulSoup
from bot import send_message
from datetime import datetime
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

URL = "https://corporate.ethiopianairlines.com/AboutEthiopian/careers/vacancies/2"
DB_FILE = "jobs.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS jobs (text TEXT UNIQUE, link TEXT, found_date TEXT)')
    conn.commit()
    conn.close()

def is_new_job(job_text, link):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    exists = c.execute('SELECT 1 FROM jobs WHERE text=? AND link=?', (job_text, link)).fetchone()
    if not exists:
        c.execute('INSERT INTO jobs VALUES (?, ?, ?)', (job_text, link, datetime.now().isoformat()))
        conn.commit()
    conn.close()
    return not exists

def print_header():
    print("\n" + "="*60)
    print("🛫  ETHIOPIAN AIRLINES JOB SCRAPER")
    print("="*60)
    print(f"  📅 Time     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  🔗 Source   : {URL[:50]}...")
    print("-"*60)

def print_status(icon, message):
    print(f"  {icon} {message}")

def print_job(text):
    # Parse the job text into components
    parts = text.split(":")
    print(f"\n  {'─'*50}")
    print(f"  📌 {text}")
    print(f"  {'─'*50}")

def print_footer(found_count, total_links):
    print("-"*60)
    print(f"  📊 Summary: {found_count} matching jobs out of {total_links} links")
    print("="*60 + "\n")

async def main():
    print_header()
    init_db()
    
    await send_message("🚀 Pilot Scraper Bot has started running!")
    print_status("🚀", "Scraper started...")

    # Setup retry logic
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retry))

    try:
        response = session.get(URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Failed to fetch page: {str(e)}"
        print_status("❌", error_msg)
        await send_message(f"⚠️ {error_msg}")
        return

    print_status("✅", "Page fetched successfully")
    
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("a")
    print_status("🔍", f"Found {len(jobs)} links to scan")

    jobs_found = []
    for job in jobs:
        text = job.get_text(strip=True)
        text_lower = text.lower()
        if "pilot" in text_lower and "trainee" in text_lower:
            link = urljoin(URL, job.get("href", ""))
            
            if is_new_job(text, link):
                jobs_found.append((text, link))
                print_status("📬", "New job detected:")
                print_job(text)

    # Send grouped notification
    if jobs_found:
        messages = []
        for text, link in jobs_found:
            messages.append(f"📋 *{text}*\n🔗 [Apply Here]({link})")
        
        grouped_message = f"🚀 *{len(jobs_found)} New Pilot Job(s) Found!*\n\n" + "\n\n".join(messages)
        grouped_message += f"\n\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        await send_message(grouped_message)
    else:
        print_status("ℹ️", "No new Pilot Trainee jobs found")
    
    print_footer(len(jobs_found), len(jobs))

if __name__ == "__main__":
    asyncio.run(main())