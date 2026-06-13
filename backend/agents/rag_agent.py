import requests
from typing import List

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

SYSTEM_PROMPT = """You are an intelligent assistant with access to tools.
When given a question, first decide which tool to use:

TOOLS AVAILABLE:
1. search_document — use this for questions about the uploaded document
2. answer_directly — use this for general knowledge questions

Respond with ONLY one of these two words first:
- "SEARCH" if you should search the document
- "DIRECT" if you can answer directly

Then on the next line write your answer or "SEARCHING..." if you chose SEARCH.

Example 1:
Question: What are the bug fixes?
SEARCH
SEARCHING...

Example 2:
Question: What is the capital of France?
DIRECT
Paris is the capital of France.
"""

def decide_and_answer(question: str, chunks: List[dict]) -> dict:
    # Step 1 — Ask agent to decide which tool to use
    decision_prompt = f"{SYSTEM_PROMPT}\n\nQuestion: {question}"

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": decision_prompt,
        "stream": False
    })

    agent_response = response.json().get("response", "").strip()
    lines = agent_response.split("\n")
    decision = lines[0].strip().upper()

    # Step 2 — Execute the right tool
    if "SEARCH" in decision:
        # Use document chunks to answer
        if not chunks:
            return {
                "tool_used": "search_document",
                "answer": "I could not find relevant content in the document.",
                "reasoning": "Searched document but found no relevant chunks."
            }

        context = ""
        for i, chunk in enumerate(chunks):
            context += f"\n--- Chunk {i + 1} ---\n{chunk['text']}\n"

        answer_prompt = f"""Answer this question using only the context below.
If the answer is not in the context say "I could not find this in the document."

Context:
{context}

Question: {question}

Answer:"""

        answer_response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": answer_prompt,
            "stream": False
        })

        answer = answer_response.json().get("response", "").strip()

        return {
            "tool_used": "search_document",
            "answer": answer,
            "reasoning": "Question was about the document so I searched it."
        }

    else:
        # Answer directly from general knowledge
        direct_prompt = f"Answer this question clearly in 2-3 sentences: {question}"

        direct_response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": direct_prompt,
            "stream": False
        })

        answer = direct_response.json().get("response", "").strip()

        return {
            "tool_used": "answer_directly",
            "answer": answer,
            "reasoning": "Question was general knowledge, no document search needed."
        }