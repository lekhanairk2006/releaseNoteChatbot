import requests
from typing import List

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

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

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code == 200:
        return response.json().get("response", "No answer generated.")
    else:
        return f"Error generating answer: {response.status_code}"