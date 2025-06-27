---
title: Virtual TA
emoji: 📚
colorFrom: pink
colorTo: indigo
sdk: docker
sdk_version: "4.16.0"
app_file: app.py
pinned: false
---


✅ 📄 Example README.md Snippet
markdown
Copy
Edit
## 🔗 API Usage

You can query the deployed Virtual TA using a simple POST request. The API accepts a student question (text) and an optional base64-encoded image (e.g., a screenshot of a Discourse post).

### Endpoint

POST https://mahakmehh-virtual-ta.hf.space/api/

pgsql
Copy
Edit

### Request Format (JSON)

```json
{
  "question": "Which model should I use?",
  "image": ""
}
Example cURL Command
bash
Copy
Edit
curl -X POST https://mahakmehh-virtual-ta.hf.space/api/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Which model should I use?", "image": ""}'
Response Format
json
Copy
Edit
{
  "answer": "You should use `gpt-3.5-turbo` for this assignment.",
  "links": [
    {
      "url": "https://discourse.example.com/t/question-id",
      "text": "Clarification on model usage"
    }
  ]
}
⏱️ The response is returned within 30 seconds, depending on system load and input size.
