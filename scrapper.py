import asyncio
import requests
from bs4 import BeautifulSoup
from bot import send_message
from datetime import datetime

URL = "https://corporate.ethiopianairlines.com/AboutEthiopian/careers/vacancies/2"

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
    
    # Notify bot that scraper started
    await send_message("🚀 Pilot Scraper Bot has started running!")
    print_status("🚀", "Scraper started...")

    response = requests.get(URL)

    if response.status_code != 200:
        print_status("❌", f"Failed to fetch page (HTTP {response.status_code})")
        await send_message(f"⚠️ Failed to fetch page: {response.status_code}")
        return

    print_status("✅", "Page fetched successfully")
    
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("a")
    print_status("🔍", f"Found {len(jobs)} links to scan")

    found_count = 0
    for job in jobs:
        text = job.get_text(strip=True)
        text_lower = text.lower()
        if "pilot" in text_lower and "trainee" in text_lower:
            link = job.get("href")
            message = f"🚀 New Job Found!\n{text}\nLink: {link}"
            await send_message(message)
            print_status("📬", "Notification sent:")
            print_job(text)
            found_count += 1

    if found_count == 0:
        print_status("ℹ️", "No Pilot Trainee jobs found today")
        await send_message("ℹ️ No Pilot Trainee jobs found today.")
    
    print_footer(found_count, len(jobs))

if __name__ == "__main__":
    asyncio.run(main())