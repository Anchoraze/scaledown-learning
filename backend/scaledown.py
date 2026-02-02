import os
import requests

SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")

def scaledown_compress(text):
    response = requests.post(
        "https://api.scaledown.ai/compress",
        headers={
            "Authorization": f"Bearer {SCALEDOWN_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "text": text,
            "target": "pedagogical",
            "compression_ratio": 0.3
        }
    )

    if response.status_code != 200:
        return text

    return response.json().get("compressed_text", text)
