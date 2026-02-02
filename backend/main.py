from fastapi import FastAPI
from backend.scaledown import scaledown_compress


app = FastAPI()

@app.get("/")
def root():
    return {"message": "ScaleDown Learning Backend Running"}

@app.post("/compress")
def compress(text: str):
    compressed = scaledown_compress(text)
    return {
        "original_length": len(text),
        "compressed_length": len(compressed),
        "compressed_text": compressed
    }
