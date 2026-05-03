import schedule
import time
import subprocess
import sys
import os

# Get the path to the current Python interpreter (the venv one)
PYTHON_EXE = sys.executable

def run_scrapers():
    print(f"\n{'-'*30}")
    print(f"⏰ Scheduler triggered at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Run the Newegg Scraper
    print("🚀 Starting Newegg Scrape...")
    subprocess.run([PYTHON_EXE, "scrapers/newegg_scraper.py"])
    
    # 2. Run the Amazon Scraper
    print("🚀 Starting Amazon Scrape...")
    subprocess.run([PYTHON_EXE, "scrapers/amazon_scraper.py"])
    
    print("✅ All scrapers finished. Returning to standby.")
    print(f"{'-'*30}\n")

# --- DEFINE THE FREQUENCY ---
# For testing, we'll run it every 2 minutes. 
# In production, you'd change this to .hours(6) or .day.at("00:00")
schedule.every(2).minutes.do(run_scrapers)

if __name__ == "__main__":
    print("🛰️  RigRadar Scheduler is now ONLINE.")
    print("The system will automatically update prices every 2 minutes.")
    print("Press Ctrl+C to stop the scheduler.")
    
    # Run once immediately so we don't have to wait 2 minutes for the first test
    run_scrapers()

    # The infinite loop that keeps the heart beating
    while True:
        schedule.run_pending()
        time.sleep(1)