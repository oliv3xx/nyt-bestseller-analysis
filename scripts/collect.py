import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("NYT_API_KEY")

LISTS = ["hardcover-fiction", "hardcover-nonfiction"]
BASE_URL = "https://api.nytimes.com/svc/books/v3/lists"
STOP_DATE = "2008-06-08"
RAW_DIR = "data/raw"

def fetch_list(list_name, date):
    url = f"{BASE_URL}/{date}/{list_name}.json"
    response = requests.get(url, params={"api-key": KEY})

    if response.status_code == 429:
        print("Hit the daily limit. Run again tomorrow to continue.")
        raise SystemExit

    response.raise_for_status()
    time.sleep(12)
    return response.json()["results"]

def collect(list_name):
    folder = os.path.join(RAW_DIR, list_name)
    os.makedirs(folder, exist_ok=True)

    date = "current"
    while date and (date == "current" or date >= STOP_DATE):
        path = os.path.join(folder, f"{date}.json")

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