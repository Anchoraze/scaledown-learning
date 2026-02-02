from fastapi import FastAPI
from pydantic import BaseModel

from backend.scaledown import scaledown_compress
from backend.books import list_books, load_book
from backend.chunking import chunk_text
from backend.store import save_chunks, get_chunks


app = FastAPI(title="ScaleDown Learning Platform")


# ---------- Models ----------

class BookRequest(BaseModel):
    book_id: str


class CompressRequest(BaseModel):
    text: str


# ---------- Routes ----------

@app.get("/")
def root():
    return {"message": "ScaleDown Learning Backend Running"}


@app.get("/books")
def books():
    """
    List available textbooks
    """
    return {"books": list_books()}


@app.post("/select_book")
def select_book(req: BookRequest):
    book_id = req.book_id

    try:
        text = load_book(book_id)
        print("BOOK LOADED")

        chunks = chunk_text(text)
        print("CHUNKED:", len(chunks))

        compressed_chunks = [scaledown_compress(c) for c in chunks]
        print("COMPRESSED")

        save_chunks(book_id, compressed_chunks)
        print("SAVED")

        return {
            "book": book_id,
            "original_chunks": len(chunks),
            "compressed_chunks": len(compressed_chunks)
        }

    except Exception as e:
        return {
            "error": str(e)
        }



@app.post("/compress")
def compress(req: CompressRequest):
    """
    Direct compression endpoint (for testing ScaleDown)
    """
    compressed = scaledown_compress(req.text)

    return {
        "original_length": len(req.text),
        "compressed_length": len(compressed),
        "compressed_text": compressed
    }


@app.get("/chunks/{book_id}")
def get_book_chunks(book_id: str):
    """
    Retrieve stored compressed chunks for a book
    """
    chunks = get_chunks(book_id)

    if not chunks:
        return {"error": "No chunks found for this book"}

    return {
        "book": book_id,
        "chunks": chunks
    }
