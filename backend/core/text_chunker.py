from typing import List

def chunk_text(text: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def chunk_document(text: str, filename: str) -> List[dict]:
    chunks = chunk_text(text)
    result = []

    for i, chunk in enumerate(chunks):
        result.append({
            "chunk_id": f"{filename}_chunk_{i}",
            "filename": filename,
            "chunk_index": i,
            "text": chunk,
            "word_count": len(chunk.split())
        })

    return result