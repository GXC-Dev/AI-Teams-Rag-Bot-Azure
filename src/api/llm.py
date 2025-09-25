
import os, requests

AOAI_ENDPOINT = os.environ["AOAI_ENDPOINT"].rstrip("/")
AOAI_KEY = os.environ["AOAI_KEY"]
AOAI_CHAT_DEPLOYMENT = os.environ["AOAI_CHAT_DEPLOYMENT"]

def chat(messages):
    url = f"{AOAI_ENDPOINT}/openai/deployments/{AOAI_CHAT_DEPLOYMENT}/chat/completions?api-version=2024-12-01-preview"
    headers = {"api-key": AOAI_KEY, "Content-Type": "application/json"}
    body = {
        "messages": messages,
        "temperature": float(os.getenv("TEMPERATURE","0")),
        "max_tokens": int(os.getenv("MAX_TOKENS","1200"))
    }
    r = requests.post(url, headers=headers, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
