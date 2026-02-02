from fastapi import FastAPI
from pydantic import BaseModel

from backend.scaledown import scaledown_compress
from backend.books import list_books, load_book
from backend.chunking import chunk_text
from backend.store import save_chunks, get_chunks
from backend.retrieval import similarity
from backend.llm import generate_answer


app = FastAPI(title="ScaleDown Learning Platform")


# ---------- Models ----------

class BookRequest(BaseModel):
    book_id: str


class CompressRequest(BaseModel):
    text: str


class AskRequest(BaseModel):
    book_id: str
    question: str


# ---------- Helpers ----------

def build_context(book_id: str, top_k: int = 3) -> str:
    chunks = get_chunks(book_id)
    if not chunks:
        return ""
    return "\n\n".join(ch["original"] for ch in chunks[:top_k])


def rank_chunks(question: str, book_id: str, top_k: int = 3):
    compressed_q = scaledown_compress(question)
    chunks = get_chunks(book_id)

    scored = []
    for ch in chunks:
        score = similarity(compressed_q, ch["compressed"])
        scored.append((score, ch))

    return sorted(scored, reverse=True)[:top_k]


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
    ranked = rank_chunks(req.question, req.book_id)

    if not ranked:
        return {"error": "No chunks for this book"}

    confidence = max(s for s, _ in ranked)
    context = "\n\n".join(ch["original"] for _, ch in ranked)

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
def generate_practice(req: AskRequest):
    ranked = rank_chunks(req.question, req.book_id)
    context = "\n\n".join(ch["original"] for _, ch in ranked)

    prompt = """
    Generate 3 practice problems based ONLY on the context.
    Include answers at the end.
    Difficulty: medium.
    """

    problems = generate_answer(prompt, context)
    return {"problems": problems}


@app.post("/quiz")
def quiz(req: AskRequest):
    context = build_context(req.book_id)

    quiz = generate_answer(
        """
        Generate 5 MCQs in STRICT JSON format:
        [
          {
            "question": "",
            "options": ["", "", "", ""],
            "answer": ""
          }
        ]
        """,
        context
    )

    return {"quiz": quiz}


@app.post("/submit_answer")
def submit_answer(data: dict):
    # Hackathon-safe stub
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
