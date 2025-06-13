
import requests
import os
from typing import List, Dict
from rag.config import settings

class Generator:
    def __init__(self):
        self.api_base_url = settings.API_BASE_URL  # Example: https://aipipe.org/openai/v1
        self.api_key = os.getenv("AIPROXY_TOKEN")  # Set this to your AI Pipe token

        if not self.api_key:
            raise EnvironmentError("❌ AIPROXY_TOKEN is not set in environment variables.")

    def generate_response(self, question: str, contexts: List[Dict]) -> Dict:
        formatted_contexts = "\n\n".join(
            f"Source {i+1} ({ctx['metadata']['source']}):\n{ctx['content']}\n"
            for i, ctx in enumerate(contexts)
        )

        payload = {
            "model": settings.LLM_MODEL,  # e.g., "openai/gpt-4o-mini"
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful TA for IIT Madras' Data Science program. "
                        "Answer questions using only the provided contexts. "
                        "For coding questions, provide complete code examples with markdown formatting."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nContexts:\n{formatted_contexts}",
                },
            ],
            "temperature": 0.3,
            "max_tokens": 500,
        }

        headers = {
            "Authorization": f"{self.api_key}",
            "Content-Type": "application/json",
        }

        endpoint = f"{self.api_base_url}/chat/completions"
        print(f"🔗 Requesting: {endpoint}")
        print(f"🔑 Using token:  {self.api_key[:6]}...")

        response = requests.post(
            endpoint,
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"❌ AI Pipe request failed: {response.status_code} - {response.text}")

        data = response.json()

        return {
            "answer": data["choices"][0]["message"]["content"],
            "sources": [
                {
                    "url": ctx["metadata"]["url"],
                    "title": ctx["metadata"]["title"],
                    "score": ctx["score"]
                }
                for ctx in contexts
            ]
        }
