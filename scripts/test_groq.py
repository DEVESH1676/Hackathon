import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
model = "llama3-70b-8192"

print(f"Testing Groq with key: {api_key[:10]}...")

resp = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={
        "model": model,
        "messages": [{"role": "user", "content": "hello"}],
        "temperature": 0.1,
    }
)

print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")
