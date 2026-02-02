from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.scaledown import scaledown_compress
from backend.books import list_books, load_book
from backend.chunking import chunk_text
from backend.store import save_chunks, get_chunks
from backend.retrieval import similarity
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

class CompressRequest(BaseModel):
    text: str

class AskRequest(BaseModel):
    book_id: str
    question: str


# ---------- Helpers ----------

def rank_chunks(book_id: str, question: str, top_k: int = 3):
    chunks = get_chunks(book_id)
    if not chunks:
        return []

    query = question.lower()
    scored = [
        (similarity(query, ch["compressed"]), ch)
        for ch in chunks
    ]
    return sorted(scored, reverse=True)[:top_k]


def build_context(book_id: str, top_k: int = 3) -> str:
    chunks = get_chunks(book_id)
    if not chunks:
        return ""
    return "\n\n".join(ch["original"] for ch in chunks[:top_k])



# ---------- Routes ----------

@app.get("/")
def root():
    return {"message": "ScaleDown Learning Backend Running"}

@app.get("/books")
def books():
    return {"books": list_books()}


@app.post("/select_book")
def select_book(req: BookRequest):
    try:
        text = load_book(req.book_id)
        chunks = chunk_text(text)

        stored_chunks = []
        for c in chunks:
            compressed = scaledown_compress(c)
            stored_chunks.append({
                "original": c,
                "compressed": compressed
            })

        save_chunks(req.book_id, stored_chunks)

        return {
            "book": req.book_id,
            "original_chunks": len(chunks),
            "compressed_chunks": len(stored_chunks)
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/compress")
def compress(req: CompressRequest):
    compressed = scaledown_compress(req.text)
    return {
        "original_length": len(req.text),
        "compressed_length": len(compressed),
        "compressed_text": compressed
    }


@app.get("/chunks/{book_id}")
def get_book_chunks(book_id: str):
    chunks = get_chunks(book_id)
    if not chunks:
        return {"error": "No chunks found for this book"}
    return {"book": book_id, "chunks": chunks}


# ---------- Core Intelligence ----------

@app.post("/ask")
def ask(req: AskRequest):
    ranked = rank_chunks(req.book_id, req.question)
    if not ranked:
        return {"error": "Book not indexed. Call /select_book first."}

    context = "\n\n".join(ch["original"] for _, ch in ranked)
    confidence = max(score for score, _ in ranked)

    answer = generate_answer(req.question, context)

    return {
        "question": req.question,
        "answer": answer,
        "confidence": confidence,
        "sources": [
            {"score": s, "text": ch["original"]}
            for s, ch in ranked
        ]
    }


@app.post("/practice")
def generate_practice(req: BookRequest):
    context = build_context(req.book_id)
    if not context:
        return {"error": "Book not indexed"}

    prompt = """
Generate 5 practice questions strictly from the context.
No numericals.
No new concepts.
Only conceptual textbook questions.
Return as a numbered list.
"""

    problems = generate_answer(prompt, context)

    return {"practice": problems}



@app.post("/quiz")
def generate_quiz(req: AskRequest):
    context = build_context(req.book_id)
    if not context:
        return {"error": "Book not indexed"}

    prompt = """
Create 5 MCQs strictly from the context.
Each MCQ must have:
- question
- 4 options
- correct answer
Return plain text or JSON.
"""

    quiz = generate_answer(prompt, context)

    return {"quiz": quiz}


@app.post("/submit_answer")
def submit_answer(data: dict):
    return {
        "status": "recorded",
        "message": "Progress updated (mock)"
    }


@app.get("/peer_comparison/{user_id}")
def peer(user_id: str):
    return {
        "your_accuracy": 70,
        "peer_average": 62
    }


@app.get("/health")
def health():
    return {"status": "ok"}
