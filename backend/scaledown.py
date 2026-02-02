# backend/scaledown.py

import os
import requests

SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")

if not SCALEDOWN_API_KEY:
    raise RuntimeError("SCALEDOWN_API_KEY not set")

SCALEDOWN_URL = "https://api.scaledown.xyz/compress/raw/"

def scaledown_compress(text: str) -> str:
    payload = {
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

    response = requests.post(SCALEDOWN_URL, json=payload, headers=headers)

    # 🔥 DEBUG: print raw response once if needed
    # print(response.text)

    response.raise_for_status()
    data = response.json()

    # ✅ Correct extraction
    return data.get("data", {}).get("compressed_prompt", "")
