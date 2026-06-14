import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def check_groq_running() -> bool:
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
        return True
    except Exception:
        return False

def safe_generate(generate_func, *args, **kwargs) -> str:
    try:
        return generate_func(*args, **kwargs)
    except Exception as e:
        return f"⚠️ Error generating answer: {str(e)}"

def add_confidence_warning(answer: str, chunks: list) -> str:
    if not chunks:
        return answer
    avg_distance = sum(c["distance"] for c in chunks) / len(chunks)
    if avg_distance > 1.5:
        answer += ("\n\n⚠️ Low confidence: The retrieved chunks may not be "
                   "closely related to your question. "
                   "Please verify this answer.")
    return answer