import json
from pathlib import Path

def combine_data():
    # Load both data sources
    with open("data/discourse_cleaned.json") as f:
        discourse_data = json.load(f)
    with open("data/tds_content.json") as f:
        tds_content = json.load(f)
    
    combined = []
    
    # Process discourse posts
    for item in discourse_data:
        # Create meaningful text content from discourse posts
        text_parts = []
        if "question" in item and item["question"]:
            text_parts.append(f"QUESTION: {item['question']}")
        if "answer" in item and item["answer"]:
            text_parts.append(f"ANSWER: {item['answer']}")
        
        combined.append({
            "text": "\n\n".join(text_parts) if text_parts else "No content",
            "title": item.get("title", "Untitled Discourse Post"),
            "url": item.get("url", "#"),
            "source": "discourse",
            "metadata": {
                "type": "discourse_post",
                "topic_id": item.get("topic_id"),
                "dates": {
                    "posted": item.get("question_date"),
                    "answered": item.get("answer_date")
                }
            }
        })
    
    # Process course content
    for item in tds_content:
        combined.append({
            "text": item.get("content", "No content available"),
            "title": f"{item.get('section', 'Course Content')} - {item.get('subsection', '')}",
            "url": f"https://course.onlinedegree.iitm.ac.in{item.get('slug', '')}",
            "source": "course_content",
            "metadata": {
                "type": "course_material",
                "section": item.get("section"),
                "subsection": item.get("subsection")
            }
        })
    
    # Save processed data
    Path("data/processed").mkdir(exist_ok=True)
    with open("data/processed/combined.json", "w") as f:
        json.dump(combined, f, indent=2)
    
    print(f"Successfully combined {len(discourse_data)} discourse posts with {len(tds_content)} course items")

if __name__ == "__main__":
    combine_data()