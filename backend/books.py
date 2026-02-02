# backend/books.py
import os 
BOOKS = {
    "physics": "OpenStax Physics textbook content here...",
    "math": "OpenStax Mathematics textbook content here..."
}

def list_books():
    return list(BOOKS.keys())

def load_book(book_id: str) -> str:
    path = f"data/books/{book_id}.txt"
    if not os.path.exists(path):
        raise ValueError("Book not found")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()
