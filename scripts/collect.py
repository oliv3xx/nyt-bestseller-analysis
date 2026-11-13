# Collects weekly NYT Best Sellers lists (2008 to now) and saves each week as raw JSON.
# Resumable: rerun after hitting the daily API limit and it skips weeks already saved.

import os
import json
import time
import requests
from dotenv import load_dotenv

# key is stored in .env so it never ends up in the code or on GitHub
load_dotenv()
KEY = os.getenv("NYT_API_KEY")

LISTS = ["hardcover-fiction", "hardcover-nonfiction"]
BASE_URL = "https://api.nytimes.com/svc/books/v3/lists"
STOP_DATE = "2008-06-08"   # oldest list available in the API
RAW_DIR = "data/raw"

def fetch_list(list_name, date):
    url = f"{BASE_URL}/{date}/{list_name}.json"
    response = requests.get(url, params={"api-key": KEY})

    # 429 = too many requests. Stop cleanly so the run can be resumed later
    if response.status_code == 429:
        print("Hit the daily limit. Run again tomorrow to continue.")
        raise SystemExit

    response.raise_for_status()
    time.sleep(12)   # API allows 5 calls per minute
    return response.json()["results"]

def collect(list_name):
    folder = os.path.join(RAW_DIR, list_name)
    os.makedirs(folder, exist_ok=True)

    # start at the current list and walk backward using NYT's own previous dates
    date = "current"
    while date and (date == "current" or date >= STOP_DATE):
        path = os.path.join(folder, f"{date}.json")

        # already saved: read from disk instead of spending an API call
        if os.path.exists(path):
            with open(path) as f:
                results = json.load(f)
        else:
            results = fetch_list(list_name, date)
            path = os.path.join(folder, f"{results['published_date']}.json")
            with open(path, "w") as f:
                json.dump(results, f)
            print(list_name, results["published_date"])

        date = results["previous_published_date"]

for list_name in LISTS:
    collect(list_name)

print("Done.")