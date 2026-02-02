import os
import requests

SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")
if not SCALEDOWN_API_KEY:
    raise RuntimeError("SCALEDOWN_API_KEY not set")

SCALEDOWN_URL = "https://api.scaledown.xyz/compress/raw/"

headers = {
    "x-api-key": SCALEDOWN_API_KEY,
    "Content-Type": "application/json"
}

def scaledown_compress(text: str):
    response = requests.post(
        SCALEDOWN_URL,
        headers=headers,
        json={
            "context": "Educational textbook compression",
            "prompt": text,
            "model": "gpt-4o",
            "scaledown": {"rate": "auto"}
        },
        timeout=30
    )

    data = response.json()
    print("RAW SCALEDOWN RESPONSE:", data)

    if "results" not in data:
        raise RuntimeError(f"ScaleDown API error: {data}")

    return data["results"]["compressed_prompt"]
