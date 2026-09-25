import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_llm(prompt: str):
    start = time.perf_counter()

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    latency_ms = (time.perf_counter() - start) * 1000

    usage = getattr(response, "usage_metadata", None)

    input_tokens = getattr(usage, "prompt_token_count", 0) if usage else 0
    output_tokens = getattr(usage, "candidates_token_count", 0) if usage else 0

    return {
        "answer": response.text,
        "latency_ms": round(latency_ms, 2),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }