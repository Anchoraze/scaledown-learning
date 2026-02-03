const BASE = "http://localhost:8000";

export async function getBooks() {
  return fetch(`${BASE}/books`).then(r => r.json());
}

export async function selectBook(book_id) {
  return fetch(`${BASE}/select_book`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ book_id })
  }).then(r => r.json());
}

export async function getPractice(book_id) {
  return fetch(`${BASE}/practice`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ book_id })
  }).then(r => r.json());
}

export async function getQuiz(book_id) {
  return fetch(`${BASE}/quiz`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ book_id })
  }).then(r => r.json());
}

// 🔥 NEW: ASK QUESTION
export async function askQuestion(book_id, question) {
  return fetch(`${BASE}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ book_id, question })
  }).then(r => r.json());
}
