from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are a helpful tutor.

STRICT RULES:
- Use ONLY the provided context.
- Do NOT use outside knowledge.
- If the answer is not explicitly in the context, reply exactly:
  "Not found in the textbook".

Context:
{context}

Question:
{question}

Answer:
""".strip()

    print("\n====== LLM PROMPT ======")
    print(prompt)
    print("========================")

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        answer = completion.choices[0].message.content

        print("\n====== LLM RESPONSE ======")
        print(answer)
        print("==========================")

        # ✅ SAFETY GUARD
        if not answer or not answer.strip():
            return "Not found in the textbook"

        return answer.strip()

    except Exception as e:
        print("❌ GROQ ERROR:", e)
        return "Not found in the textbook"
