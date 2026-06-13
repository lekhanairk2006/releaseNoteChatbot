import requests

def check_ollama_running() -> bool:
    try:
        response = requests.get(
            "http://localhost:11434",
            timeout=3
        )
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.Timeout:
        return False

def safe_generate(generate_func, *args, **kwargs) -> str:
    try:
        return generate_func(*args, **kwargs)
    except requests.exceptions.ConnectionError:
        return ("⚠️ AI model is not running. "
                "Please start Ollama with: ollama serve")
    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. Please try again."
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

def add_confidence_warning(answer: str, chunks: list) -> str:
    if not chunks:
        return answer

    avg_distance = sum(c["distance"] for c in chunks) / len(chunks)

    # Higher distance means less similar
    if avg_distance > 1.5:
        answer += ("\n\n⚠️ Low confidence: The retrieved chunks may not be "
                   "closely related to your question. "
                   "Please verify this answer.")
    return answer