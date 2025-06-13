# scraper/scrape_discourse.py
from datetime import datetime, timezone
import requests
import time
import json
import os
from datetime import datetime
from config import HEADERS, BASE_URL, CATEGORY_SLUG

# Constants

START_DATE = datetime(2025, 1, 1, tzinfo=timezone.utc)
END_DATE = datetime(2025, 4, 14, tzinfo=timezone.utc)

# Ensure output folder exists
os.makedirs("data", exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)

def fetch_topic_ids(category_slug):
    topic_ids = []
    page = 0

    while True:
        page += 1
        url = f"{BASE_URL}/{category_slug}.json?page={page}"
        print(f"📄 Fetching topic list: {url}")
        response = session.get(url)

        if response.status_code != 200:
            print(f"❌ Failed to fetch topic list page {page}: {response.status_code}")
            break

        data = response.json()
        topics = data.get("topic_list", {}).get("topics", [])
        if not topics:
            break

        topic_ids.extend([t["id"] for t in topics])
        time.sleep(1.5)

    return topic_ids

def fetch_topic_details(topic_id):
    url = f"{BASE_URL}/t/{topic_id}.json"
    print(f"🔍 Fetching topic {topic_id}")
    response = session.get(url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch topic {topic_id}: {response.status_code}")
        return None
    return response.json()

def clean_post(post):
    return {
        "post_number": post["post_number"],
        "username": post["username"],
        "created_at": post["created_at"],
        "cooked": post["cooked"],
    }

def is_within_date_range(date_str):
    post_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return START_DATE <= post_date <= END_DATE

def scrape_discourse():
    all_data = []
    topic_ids = fetch_topic_ids(CATEGORY_SLUG)

    print(f"🧵 Found {len(topic_ids)} topics. Checking dates...")
    for idx, topic_id in enumerate(topic_ids):
        try:
            topic_json = fetch_topic_details(topic_id)
            if not topic_json:
                continue

            first_post_date = topic_json["post_stream"]["posts"][0]["created_at"]
            if not is_within_date_range(first_post_date):
                continue  # skip out-of-range topics

            topic_data = {
                "topic_id": topic_id,
                "title": topic_json["title"],
                "url": f"{BASE_URL}/t/{topic_id}",
                "posts": [clean_post(p) for p in topic_json["post_stream"]["posts"]],
            }

            all_data.append(topic_data)
            time.sleep(1.5)

        except Exception as e:
            print(f"⚠️ Error with topic {topic_id}: {e}")

    with open("data/discourse_raw.json", "w") as f:
        json.dump(all_data, f, indent=2)

    print(f"✅ Scraping complete! Saved {len(all_data)} filtered topics to data/discourse_raw.json")

if __name__ == "__main__":
    scrape_discourse()
