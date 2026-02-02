# backend/chunking.py

def chunk_text(text: str, max_length: int = 500):
    """
    Splits text into semantic-ish chunks of ~max_length characters
    """
    chunks = []
    current = ""

    for paragraph in text.split("\n"):
        if len(current) + len(paragraph) < max_length:
            current += paragraph + "\n"
        else:
            chunks.append(current.strip())
            current = paragraph + "\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks
