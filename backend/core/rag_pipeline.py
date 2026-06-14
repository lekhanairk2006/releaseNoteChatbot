import os
from groq import Groq
from dotenv import load_dotenv
from typing import List

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt(question: str, chunks: List[dict]) -> str:
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"\n--- Chunk {i + 1} ---\n{chunk['text']}\n"

    prompt = f"""You are a helpful assistant. Answer the question using 
only the context below. If the answer is not in the context, say 
"I could not find this information in the document."

Context:
{context}

Question: {question}

Answer:"""
    return prompt

def generate_answer(question: str, chunks: List[dict]) -> str:
    if not chunks:
        return "I could not find any relevant content in the document."

    prompt = build_prompt(question, chunks)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )

    return response.choices[0].message.content