# Pilot Job Scraper & Telegram Notifier

> From the desk of a  Backend Engineer: this repo is small, ruthless, and gets the job done — it scrapes a careers page and pings you on Telegram when something interesting for pilots shows up. It's opinionated, slightly arrogant, and reliable when treated with respect.

---

## The one-liner
A tiny Python service that fetches a target careers page on a schedule, parses job postings, filters by role keywords, and notifies a Telegram chat when matches are found.

## Why this exists (and why it's clever)
- You want to be the first to know when pilot roles drop.
- It's tiny, easy to run locally or on a cheap VPS, and integrates with Telegram so you don't need to babysit email.
- Uses plain, well-known libraries (requests, BeautifulSoup, python-telegram-bot, APScheduler) so debugging is fast.

---

## Features
- Cron-like scheduler (APS cheduler) to run scraping jobs on a schedule.
- Simple HTML parsing with BeautifulSoup and flexible keyword matching.
- Async Telegram notifications using `python-telegram-bot`.
- Quick helpers to discover `CHAT_ID` values.

---

## Files you care about
- `scrapper.py` — async `main()` runner: fetches the target URL, parses anchor tags, filters for keywords, sends notifications.
- `bot.py` — Telegram wrapper: loads `BOT_TOKEN` + `CHAT_ID` from `.env` and exposes `send_message()`.
- `scheduler.py` — boots APScheduler and schedules `scrapper.main()` on cron-like rules.
- `get_chat_id.py` — helper to list updates and reveal chat IDs (useful to discover the correct `CHAT_ID`).
- `.env` — environment variables (contains secrets; do not commit).

---

## Quickstart (Windows PowerShell)
Follow me and the bot will tell you secrets. Run these from project root.

1) Create and activate a virtual environment (recommended)

```powershell
python -m venv .\venv
.\venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install requests beautifulsoup4 python-dotenv python-telegram-bot apscheduler
```

3) Create a `.env` file (DON'T CHECK IT IN)

```
BOT_TOKEN="your_bot_token"
CHAT_ID="your_chat_id"
```

4) (Optional) Discover your chat id — have the user/group send one message to the bot, then run:

```powershell
python get_chat_id.py
```

5) Sanity-run the scraper once:

```powershell
python scrapper.py
```

6) Or start the scheduler (runs on cron schedule in `scheduler.py`):

```powershell
python scheduler.py
```

---

## What I, the Senior Backend Engineer, would bitch about and fix immediately
1. Secrets: `.env` is present — rotate the token and add `.env` to `.gitignore`.
2. Deduplication: the code sends notifications every run for matching links; add persistent state (SQLite/JSON) to avoid duplicates.
3. Error handling: wrap network and Telegram calls in try/except, add retry/backoff, and log structured errors.
4. Tests: extract parsing into a pure function and add unit tests with HTML fixtures.

---

## Troubleshooting (copy/paste like a sniper)

- BeautifulSoup FeatureNotFound: make sure you're using the correct parser name:

```py
soup = BeautifulSoup(response.text, "html.parser")
```

- telegram.error.BadRequest: Chat not found — fix checklist:
  - Confirm `CHAT_ID` is correct and numeric (channels/supergroups often require `-100...`).
  - Ensure the target user started the bot (private chat) or the bot was added to the group/channel.
  - Ensure the `BOT_TOKEN` matches the bot intended to send messages.
  - Run `python get_chat_id.py` after sending a test message to the bot to capture the correct chat id.

Example defensive pattern to add to `bot.py`:

```py
from telegram import error

try:
    await bot.send_message(chat_id=CHAT_ID, text=message)
except error.BadRequest as e:
    # log context and fail gracefully
    print("BadRequest:", e)
    # optionally attempt bot.get_chat(CHAT_ID) to introspect

```

---

## Screenshots
Paste screenshots in `screenshots/` and reference them below. I left deliberate placeholders so your README looks expensive.

- Dashboard / Schedule
  ![scheduler-console](screenshots/scheduler-console.png)

- Example Telegram notification
  ![telegram-notification](screenshots/telegram-notification.png)

- HTML parsing sample (before/after)
  ![parsing-sample](screenshots/parsing-sample.png)

---

## Production notes (short & brutal)
- Run this inside a container or systemd unit.
- Use environment variables injected by your orchestrator, not a checked-in `.env`.
- Add logging, health endpoints, and alerts; monitor the job success rate.

## Minimal requirements.txt

```
requests
beautifulsoup4
python-dotenv
python-telegram-bot
apscheduler
```

---

## Contributing (how to earn my respect)
- Open a PR: small, atomic, well-tested.
- Add tests for parsing logic and CI that runs them.
- If you change behavior (keywords, notification format), document it here.

---

## License
Keep it simple. Do whatever, but don't leak tokens.

---

Made with strong opinions and a little caffeine. —  Backend Heavy DEV
