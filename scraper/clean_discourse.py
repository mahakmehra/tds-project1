import json
import os
from bs4 import BeautifulSoup
from datetime import datetime, timezone

RAW_FILE = "data/discourse_raw.json"
OUT_FILE = "data/discourse_cleaned.json"

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n").strip()

def clean_data():
    with open(RAW_FILE, "r") as f:
        topics = json.load(f)

    cleaned = []

    for topic in topics:
        q_post = topic["posts"][0]
        question = html_to_text(q_post["cooked"])
        question_date = q_post["created_at"]

        # Find the first valid reply from a staff/TA (excluding original poster)
        answer = None
        answer_date = None
        for p in topic["posts"][1:]:
            if p["username"].lower() != q_post["username"].lower():
                ans_txt = html_to_text(p["cooked"])
                if ans_txt:
                    answer = ans_txt
                    answer_date = p["created_at"]
                    break

        if answer:
            cleaned.append({
                "topic_id": topic["topic_id"],
                "title": topic["title"],
                "url": topic["url"],
                "question": question,
                "question_date": question_date,
                "answer": answer,
                "answer_date": answer_date
            })

    os.makedirs("data", exist_ok=True)
    with open(OUT_FILE, "w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Cleaned {len(cleaned)} Q&A pairs into {OUT_FILE}")

if __name__ == "__main__":
    clean_data()
