import os
import requests

SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")

SCALEDOWN_URL = "https://api.scaledown.xyz/compress/raw/"

def scaledown_compress(text: str) -> str:
    if not SCALEDOWN_API_KEY:
        raise ValueError("SCALEDOWN_API_KEY not set")

    payload = {
        "context": "Educational textbook compression. Preserve definitions, formulas, and learning value.",
        "prompt": text,
        "model": "gpt-4o",
        "scaledown": {
            "rate": "auto"
        }
    }

    headers = {
        "x-api-key": SCALEDOWN_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        SCALEDOWN_URL,
        headers=headers,
        json=payload,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    # ScaleDown usually returns compressed text here
    return data.get("output", data.get("compressed", data.get("result", "")))
