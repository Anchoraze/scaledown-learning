from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random

from backend.scaledown import scaledown_compress
from backend.books import list_books, load_book
from backend.chunking import chunk_text
from backend.store import save_chunks, get_chunks
from backend.llm import generate_answer

app = FastAPI(title="ScaleDown Learning Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------

class BookRequest(BaseModel):
    book_id: str

class AskRequest(BaseModel):
    book_id: str
    question: str = ""

# ---------- Helpers ----------

def build_context(book_id: str, top_k: int = 4) -> str:
    chunks = get_chunks(book_id)
    if not chunks:
        return ""
    random.shuffle(chunks)
    return "\n\n".join(ch["original"] for ch in chunks[:top_k])

# ---------- Routes ----------

@app.get("/books")
def books():
    return {"books": list_books()}

@app.post("/select_book")
def select_book(req: BookRequest):
    text = load_book(req.book_id)
    chunks = chunk_text(text)

    stored = []
    for c in chunks:
        stored.append({
            "original": c,
            "compressed": scaledown_compress(c)
        })

    save_chunks(req.book_id, stored)
    return {"status": "ok"}

@app.post("/practice")
def practice(req: BookRequest):
    context = build_context(req.book_id)
    if not context:
        return {"practice": []}

    prompt = """
Generate 5 conceptual practice questions strictly from the context.
Return them as a numbered list.
"""

    text = generate_answer(prompt, context)

    practice = [
        line.strip()[2:]
        for line in text.split("\n")
        if line.strip() and line[0].isdigit()
    ]

    return {"practice": practice}

@app.post("/quiz")
def quiz(req: AskRequest):
    context = build_context(req.book_id)
    if not context:
        return {"quiz": "[]"}

    prompt = """
Create 5 MCQs strictly from the context.

Return VALID JSON only in this format:

[
  {
    "question": "...",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "answerIndex": 0
  }
]

Rules:
- answerIndex must be 0-based
- No explanations
- JSON only
"""

    quiz = generate_answer(prompt, context)
    return {"quiz": quiz}

# 🔥 NEW: ASK QUESTION ENDPOINT
@app.post("/ask")
def ask(req: AskRequest):
    context = build_context(req.book_id)
    if not context:
        return {"answer": "Book not indexed."}

    prompt = f"""
You are a helpful teacher.

Answer the following question clearly and directly
using ONLY the given context.

Question:
{req.question}

Rules:
- Do NOT mention the word "context"
- Do NOT say "according to the context"
- Explain in simple textbook language
"""

    answer = generate_answer(prompt, context)

    return {"answer": answer}
