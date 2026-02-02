CHUNKS_DB = {}

def save_chunks(book_id: str, chunks: list):
    """
    chunks = [
      {"original": "...", "compressed": "..."},
      ...
    ]
    """
    CHUNKS_DB[book_id] = chunks

def get_chunks(book_id: str):
    return CHUNKS_DB.get(book_id, [])
