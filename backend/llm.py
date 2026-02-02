from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are a helpful tutor.
Answer the question ONLY using the context below.
If the answer is not present, say "Not found in the textbook".

Context:
{context}

Question:
{question}

Answer:
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # IMPORTANT
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return completion.choices[0].message.content
