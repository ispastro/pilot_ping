import asyncio
import threading
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from scrapper import main
from datetime import datetime

app = Flask(__name__)
last_run = None

# Health check route for Render
@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "service": "Ethiopian Airlines Pilot Job Scraper",
        "message": "🛫 Scraper is active and monitoring jobs!"
    })

@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "last_run": last_run.isoformat() if last_run else "Never"
    })

@app.route('/run-now')
def trigger_scraper():
    threading.Thread(target=run_scraper).start()
    return jsonify({"status": "triggered", "message": "Scraper started manually"})

# Run the async scraper in a sync context
def run_scraper():
    global last_run
    asyncio.run(main())
    last_run = datetime.now()

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(run_scraper, 'cron', day_of_week='mon,wed,fri', hour=9, minute=0)
scheduler.start()

print("🛰 Scheduler started. Waiting for the next mission...")

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
