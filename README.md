# 🎓 Educational Content Assistant

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=1000&color=38BDF8&center=true&vCenter=true&width=900&lines=AI-powered+Learning+Assistant;Ask+Questions+%7C+Practice+%7C+Quiz;ScaleDown+Compression+%7C+Groq+LLMs" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-success" />
  <img src="https://img.shields.io/badge/AI-Groq-orange" />
  <img src="https://img.shields.io/badge/Compression-ScaleDown-blue" />
</p>

---

## ✨ What is Educational Content Assistant?

**Educational Content Assistant** is an AI‑powered learning platform that lets students:

- 📖 Load textbooks
- 💬 Ask natural‑language questions
- 🧠 Get context‑aware AI answers
- 📝 Generate practice questions
- 🎯 Attempt MCQ quizzes with live accuracy tracking

All while **reducing textbook size by ~70% using ScaleDown compression** ⚡

---

## 🚀 Unique Selling Points (USP)

### 🗜️ ScaleDown Compression (70% reduction)
- Textbooks are **compressed semantically**, not truncated
- Preserves learning value while drastically reducing token usage
- Faster responses + lower LLM cost

> 📉 Result: Smaller context → faster Groq inference → smoother UX

---

### ⚡ Groq‑Powered LLM Inference
- Ultra‑fast responses using **Groq API**
- Used for:
  - Answering questions
  - Generating practice problems
  - Creating MCQ quizzes

> ⏱️ Near‑instant answers even on large books

---

### 🧩 Context‑Aware Retrieval
- Book is chunked and stored
- Relevant sections are randomly sampled
- Prevents hallucination by **answering strictly from book context**

---

## 🧠 Features

### ❓ Ask Questions
- Ask anything from the book
- AI answers strictly from textbook context

### 📝 Practice Mode
- Generates 5 conceptual questions
- Great for revision

### 🎯 Quiz Mode
- 5 MCQs per quiz
- Individual submission per question
- Accuracy & progress tracking

---

## 🛠️ Tech Stack

### Backend
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" height="40" />
</p>

### Frontend
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" height="40" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" height="40" />
</p>

### AI & Infra
<p>
  <img src="https://assets-global.website-files.com/64f8f8cbe8c9d58c3f20a5f4/64f8fa1c3f2f7e6d91b1b3aa_groq-logo.svg" height="40" />
  <img src="https://img.shields.io/badge/ScaleDown-Compression-blue" />
</p>

---

## 📁 Project Structure

```
backend/
 ├── main.py        # FastAPI server
 ├── llm.py         # Groq LLM integration
 ├── scaledown.py   # 70% compression logic
 ├── chunking.py    # Text chunking
 ├── retrieval.py   # Context retrieval
 ├── store.py       # Chunk storage
 └── books.py       # Book loader

frontend/
 └── src/
     ├── App.jsx
     ├── api.js
     └── App.css
```

---

## ⚙️ Running Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📈 Why This Project Matters

- Reduces AI cost using compression
- Improves learning efficiency
- Shows real‑world AI system design
- Combines **ML + Backend + Frontend**

Perfect for:
- 🧑‍🎓 Students
- 👨‍💻 AI Engineers
- 📚 EdTech platforms

---

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=22C55E&center=true&vCenter=true&width=700&lines=Learn+Smarter.;Ask+Better.;Scale+Efficiently." />
</p>

