import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

JEV_API_KEY = os.getenv("JEV_API_KEY")
print("JEV KEY LOADED:", bool(JEV_API_KEY))
print(
    "JEV KEY PREFIX:",
    JEV_API_KEY[:8] if JEV_API_KEY else "NONE"
)

JEV_URL = "https://thejevai.com/v1/systemone"


def ask_jev(query: str, question: dict):
    payload = {
        "model": "jev-latest",
        "state": query,
        "questions": {
            "decision": question
        }
    }

    headers = {
        "Authorization": f"Bearer {JEV_API_KEY}",
        "Content-Type": "application/json"
    }

    start = time.perf_counter()

    response = requests.post(
        JEV_URL,
        json=payload,
        headers=headers,
        timeout=30
    )

    latency_ms = (time.perf_counter() - start) * 1000

    if not response.ok:
        print("JEV STATUS:", response.status_code)
        print("JEV RESPONSE:", response.text)

    response.raise_for_status()

    data = response.json()

    return {
        "response": data,
        "latency_ms": round(latency_ms, 2)
    }