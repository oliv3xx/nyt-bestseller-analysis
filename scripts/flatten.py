# flattens raw NYT list JSON files into one CSV (one row per book per week)
import os
import json
import pandas as pd

RAW_DIR = "data/raw"
OUT_PATH = "data/clean/weekly_rankings.csv"

# read every saved week for each list and flatten it into one row per book
rows = []

for list_name in os.listdir(RAW_DIR):
    folder = os.path.join(RAW_DIR, list_name)

    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename)) as f:
            results = json.load(f)

        for book in results["books"]:
            # .get() returns None for missing fields instead of crashing (older lists have gaps)
            rows.append({
                "list_name": list_name,
                "published_date": results["published_date"],
                "rank": book.get("rank"),
                "rank_last_week": book.get("rank_last_week"),
                "weeks_on_list": book.get("weeks_on_list"),
                "title": book.get("title"),
                "author": book.get("author"),
                "publisher": book.get("publisher"),
                "isbn13": book.get("primary_isbn13"),
                "isbn10": book.get("primary_isbn10"),
            })

df = pd.DataFrame(rows)
# sort so the CSV reads in order: list, week, rank
df = df.sort_values(["list_name", "published_date", "rank"])
df.to_csv(OUT_PATH, index=False)

print(len(df), "rows")
print(df["isbn13"].nunique(), "unique books")
print(df.head())