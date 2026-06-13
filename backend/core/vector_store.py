import os
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List

# Load the free local embedding model
# Downloads once (~90MB), then runs offline forever
model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="./chroma_db")

def get_collection(filename: str):
    name = filename.replace(".", "_").replace(" ", "_")
    return chroma_client.get_or_create_collection(name=name)

def get_embedding(text: str) -> List[float]:
    embedding = model.encode(text)
    return embedding.tolist()

def store_chunks(chunks: List[dict], filename: str):
    collection = get_collection(filename)

    # Clear existing chunks for this file
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["chunk_id"] for chunk in chunks]
    metadatas = [{"filename": chunk["filename"],
                  "chunk_index": chunk["chunk_index"]} for chunk in chunks]

    embeddings = [get_embedding(text) for text in texts]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    return len(chunks)

def search_chunks(query: str, filename: str, top_k: int = 3) -> List[dict]:
    collection = get_collection(filename)
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks = []
    for i, doc in enumerate(results["documents"][0]):
        chunks.append({
            "text": doc,
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "distance": results["distances"][0][i]
        })

    return chunks