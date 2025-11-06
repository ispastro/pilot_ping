import asyncio
import requests
from bs4 import BeautifulSoup
from bot import send_message  # async function

URL = "https://corporate.ethiopianairlines.com/AboutEthiopian/careers/vacancies/2"

async def main():
    # Notify bot that scraper started
    await send_message("🚀 Pilot Scraper Bot has started running!")

    print("Scraper running... fetching jobs")
    response = requests.get(URL)

    if response.status_code != 200:
        print("Failed to fetch page:", response.status_code)
        await send_message(f"⚠️ Failed to fetch page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("a")
    print(f"Found {len(jobs)} total links on the page")

    found_any = False
    for job in jobs:
        text = job.get_text(strip=True)
        text_lower = text.lower()
        if "Pilot trainee" in text_lower and "aircraft maintenance" in text_lower:
            link = job.get("href")
            message = f"🚀 New Job Found!\n{text}\nLink: {link}"
            await send_message(message)
            print("Notification sent for:", text)
            found_any = True

    if not found_any:
        print("No Pilot Trainee or aircraft maintenance jobs found today.")
        await send_message("ℹ️ No Pilot Trainee jobs found today.")

# Run the async main function
asyncio.run(main())
