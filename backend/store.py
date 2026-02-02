# backend/store.py

CHUNKS_DB = {}

def save_chunks(book_name: str, chunks: list):
    CHUNKS_DB[book_name] = chunks

def get_chunks(book_name: str):
    return CHUNKS_DB.get(book_name, [])
