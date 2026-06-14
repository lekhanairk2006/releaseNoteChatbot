import os
from groq import Groq
from dotenv import load_dotenv
from typing import List

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
Paris is the capital of France."""

def decide_and_answer(question: str, chunks: List[dict]) -> dict:
    # Step 1 — Ask agent to decide which tool to use
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Question: {question}"}
        ],
        max_tokens=256
    )

    agent_response = response.choices[0].message.content.strip()
    lines = agent_response.split("\n")
    decision = lines[0].strip().upper()

    # Step 2 — Execute the right tool
    if "SEARCH" in decision:
        if not chunks:
            return {
                "tool_used": "search_document",
                "answer": "I could not find relevant content in the document.",
                "reasoning": "Searched document but found no relevant chunks."
            }

        context = ""
        for i, chunk in enumerate(chunks):
            context += f"\n--- Chunk {i + 1} ---\n{chunk['text']}\n"

        answer_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": f"""Answer this question using 
only the context below. If the answer is not in the context say 
"I could not find this in the document."

Context:
{context}

Question: {question}

Answer:"""}
            ],
            max_tokens=1024
        )

        return {
            "tool_used": "search_document",
            "answer": answer_response.choices[0].message.content.strip(),
            "reasoning": "Question was about the document so I searched it."
        }

    else:
        direct_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": f"Answer this question clearly in 2-3 sentences: {question}"}
            ],
            max_tokens=256
        )

        return {
            "tool_used": "answer_directly",
            "answer": direct_response.choices[0].message.content.strip(),
            "reasoning": "Question was general knowledge, no document search needed."
        }