import { useEffect, useState } from "react";
import {
  getBooks,
  selectBook,
  getPractice,
  getQuiz,
  askQuestion
} from "./api";

import "./App.css";

export default function App() {
  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState("");
  const [bookLoaded, setBookLoaded] = useState(false);

  const [practice, setPractice] = useState([]);

  const [quiz, setQuiz] = useState([]);
  const [selected, setSelected] = useState({});
  const [submitted, setSubmitted] = useState({});

  const [attempted, setAttempted] = useState(0);
  const [correct, setCorrect] = useState(0);
  const [status, setStatus] = useState("");

  // 🔥 ASK STATE
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  useEffect(() => {
    getBooks().then(d => setBooks(d.books || []));
  }, []);

  async function loadBook() {
    setStatus("Loading...");
    await selectBook(selectedBook);
    setBookLoaded(true);
    setStatus("✅ Book loaded");
    setPractice([]);
    setQuiz([]);
    setAnswer("");
  }

  async function loadPractice() {
    const res = await getPractice(selectedBook);
    setPractice(res.practice || []);
  }

  async function loadQuiz() {
    const res = await getQuiz(selectedBook);
    const parsed = JSON.parse(res.quiz);
    setQuiz(parsed);
    setSelected({});
    setSubmitted({});
  }

  async function ask() {
    if (!question.trim()) return;
    setAnswer("Thinking...");
    const res = await askQuestion(selectedBook, question);
    setAnswer(res.answer || "No answer");
  }

  function submitOne(qIdx) {
    if (submitted[qIdx]) return;

    setAttempted(a => a + 1);

    if (selected[qIdx] === quiz[qIdx].answerIndex) {
      setCorrect(c => c + 1);
      alert("✅ Correct");
    } else {
      alert("❌ Wrong");
    }

    setSubmitted(s => ({ ...s, [qIdx]: true }));
  }

  return (
    <div className="container">
      <h1>📘 Educational Content Assistant</h1>

      {/* BOOK */}
      <div className="card">
        <select value={selectedBook} onChange={e => setSelectedBook(e.target.value)}>
          <option value="">Select book</option>
          {books.map(b => <option key={b}>{b}</option>)}
        </select>

        <button onClick={loadBook} disabled={!selectedBook}>Load</button>
        <p>{status}</p>
      </div>

      {/* ASK */}
      <div className="card">
        <h3>Ask a Question</h3>

        <input
          type="text"
          placeholder="Ask something from the book..."
          value={question}
          onChange={e => setQuestion(e.target.value)}
          style={{ width: "100%", padding: "10px" }}
        />

        <button onClick={ask} disabled={!bookLoaded}>
          Ask
        </button>

        {answer && <p><strong>Answer:</strong> {answer}</p>}
      </div>

      {/* PRACTICE */}
      <div className="card">
        <button onClick={loadPractice} disabled={!bookLoaded}>
          Generate Practice
        </button>

        <ul>
          {practice.map((p, i) => <li key={i}>{p}</li>)}
        </ul>
      </div>

      {/* QUIZ */}
      <div className="card">
        <button onClick={loadQuiz} disabled={!bookLoaded}>
          Generate Quiz
        </button>

        {quiz.map((q, qi) => (
          <div key={qi} className="quiz">
            <h4>Q{qi + 1}. {q.question}</h4>

            {q.options.map((opt, oi) => (
              <label key={oi}>
                <input
                  type="radio"
                  name={`q${qi}`}
                  disabled={submitted[qi]}
                  checked={selected[qi] === oi}
                  onChange={() =>
                    setSelected(s => ({ ...s, [qi]: oi }))
                  }
                />
                {opt}
              </label>
            ))}

            <button
              disabled={submitted[qi] || selected[qi] == null}
              onClick={() => submitOne(qi)}
            >
              {submitted[qi] ? "Submitted" : "Submit"}
            </button>
          </div>
        ))}
      </div>

      {/* PROGRESS */}
      <div className="card">
        <h3>Progress</h3>
        <p>Attempted: {attempted}</p>
        <p>
          Accuracy: {attempted === 0 ? "—" :
            Math.round((correct / attempted) * 100) + "%"}
        </p>
      </div>
    </div>
  );
}
