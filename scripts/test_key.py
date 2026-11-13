import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("NYT_API_KEY")

url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json"
response = requests.get(url, params={"api-key": key})

print(response.status_code)
for book in response.json()["results"]["books"][:5]:
    print(book["rank"], book["title"], book["weeks_on_list"])