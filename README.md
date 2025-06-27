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

## 🔗 API Usage

You can query the deployed Virtual TA using a simple POST request.

### 📮 Endpoint
POST https://mahakmehh-virtual-ta.hf.space/api/


### 📤 Request Format (JSON)

```json
{
  "question": "Which model should I use?",
  "image": ""
}
```
### 🧪 Example cURL

```bash
curl -X POST https://mahakmehh-virtual-ta.hf.space/api/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Which model should I use?", "image": ""}'
```

📥 Response Format
```json 
{
  "answer": "You should use `gpt-3.5-turbo` for this assignment.",
  "links": [
    {
      "url": "https://discourse.example.com/t/question-id",
      "text": "Clarification on model usage"
    }
  ]
}
```
