# backend/books.py

BOOKS = {
    "physics": "OpenStax Physics textbook content here...",
    "math": "OpenStax Mathematics textbook content here..."
}

def list_books():
    return list(BOOKS.keys())

def load_book(book_name: str):
    return BOOKS.get(book_name, "Book not found")
