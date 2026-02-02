import { useEffect, useState } from "react";
import {
  getBooks,
  selectBook,
  askQuestion,
  getPractice,
  getQuiz
} from "./api";

export default function App() {
  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState("");
  const [bookLoaded, setBookLoaded] = useState(false);

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const [practice, setPractice] = useState([]);
  const [quiz, setQuiz] = useState("");


  const [status, setStatus] = useState("");

  useEffect(() => {
    getBooks().then(data => setBooks(data.books || []));
  }, []);

  async function loadBook() {
    setStatus("Loading book...");
    const res = await selectBook(selectedBook);
    if (res.error) {
      setStatus("❌ Failed to load book");
    } else {
      setBookLoaded(true);
      setStatus("✅ Book loaded");
    }
  }

  async function ask() {
    setAnswer("Thinking...");
    const res = await askQuestion(selectedBook, question);
    setAnswer(res.answer || "No answer");
  }

  async function loadPractice() {
    const res = await getPractice(selectedBook);
    setPractice(res.practice || "No practice generated");
  }

  async function loadQuiz() {
    const res = await getQuiz(selectedBook);
    setQuiz(res.quiz || "No quiz generated");
  }

  return (
    <div style={{ padding: 30, maxWidth: 800, margin: "auto" }}>
      <h1>📘 ScaleDown Learning</h1>

      {/* Book Selection */}
      <h3>Select Book</h3>
      <select
        value={selectedBook}
        onChange={e => setSelectedBook(e.target.value)}
      >
        <option value="">-- choose --</option>
        {books.map(b => (
          <option key={b} value={b}>{b}</option>
        ))}
      </select>

      <button onClick={loadBook} disabled={!selectedBook}>
        Load Book
      </button>

      <p>{status}</p>

      <hr />

      {/* Ask */}
      <h3>Ask Question</h3>
      <textarea
        rows={3}
        value={question}
        onChange={e => setQuestion(e.target.value)}
        disabled={!bookLoaded}
      />

      <br />
      <button onClick={ask} disabled={!bookLoaded || !question}>
        Ask
      </button>

      <h4>Answer</h4>
      <div style={{ background: "#222", padding: 10 }}>
        {answer}
      </div>

      <hr />

      {/* Practice */}
      <h3>Practice Problems</h3>
      <button onClick={loadPractice} disabled={!bookLoaded}>
        Generate Practice
      </button>

      <pre>{practice}</pre>

      <hr />

      {/* Quiz */}
      <h3>Quiz</h3>
      <button onClick={loadQuiz} disabled={!bookLoaded}>
        Generate Quiz
      </button>

      <pre>{quiz}</pre>

      <hr />

      {/* Dashboard placeholders */}
      <h3>Progress</h3>
      <p>Accuracy: —</p>
      <p>Questions attempted: —</p>

      <h3>Peer Comparison</h3>
      <p>Coming soon 🚀</p>
    </div>
  );
}
