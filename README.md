# 📄 ReleaseNote Chatbot

A Retrieval-Augmented Generation (RAG) system that lets you upload 
enterprise documents and ask natural language questions about them.

---

## What it does

Upload any PDF, TXT, CSV, or Excel file and ask questions in plain English.
The app finds the most relevant parts of your document and generates
accurate, grounded answers using a local AI model.

---

## Architecture

    User → Streamlit UI (port 8501)
                ↓
           FastAPI Backend (port 8000)
                ↓
        document_reader  ← reads PDF/TXT/CSV/Excel
        text_chunker     ← splits into 200-word chunks
        vector_store     ← embeds + stores in ChromaDB
        rag_agent        ← decides search vs direct answer
        rag_pipeline     ← generates answer using Ollama
                ↓
           ChromaDB (local vector database)
                ↓
           Ollama (local LLM - TinyLlama)

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Frontend | Streamlit | User interface |
| Backend | FastAPI | API server |
| Embeddings | sentence-transformers | Free local embeddings |
| Vector DB | ChromaDB | Semantic search |
| LLM | Ollama + TinyLlama | Answer generation |

---

## Project Structure

    releaseNoteChatbot/
    ├── app.py                  ← Streamlit UI
    ├── backend/
    │   ├── main.py             ← FastAPI entry point
    │   ├── api/
    │   │   └── routes.py       ← API endpoints
    │   ├── agents/
    │   │   └── rag_agent.py    ← Agent reasoning
    │   ├── core/
    │   │   ├── document_reader.py
    │   │   ├── text_chunker.py
    │   │   ├── vector_store.py
    │   │   └── rag_pipeline.py
    │   └── utils/
    │       ├── validator.py
    │       └── error_handler.py
    ├── chroma_db/              ← Vector database
    ├── uploaded_files/         ← Uploaded documents
    ├── requirements.txt
    └── .env

---

## How to Run Locally

**1. Clone the repository**

    git clone https://github.com/lekhanairk2006/releaseNoteChatbot.git
    cd releaseNoteChatbot

**2. Create virtual environment**

    python -m venv venv
    source venv/bin/activate

**3. Install dependencies**

    pip install -r backend/requirements.txt
    pip install streamlit sentence-transformers

**4. Set up environment variables**

    cp .env.example .env

**5. Install and start Ollama**

Download from https://ollama.com then:

    ollama pull tinyllama
    ollama serve

**6. Start FastAPI backend**

    uvicorn backend.main:app --reload

**7. Start Streamlit frontend**

    streamlit run app.py

**8. Open the app**

Go to http://localhost:8501

---

## How RAG Works

1. **Upload** — document is saved and text is extracted
2. **Chunk** — text is split into 200-word overlapping pieces
3. **Embed** — each chunk is converted to 384 numbers (vectors)
4. **Store** — vectors saved in ChromaDB
5. **Query** — your question is also converted to a vector
6. **Search** — ChromaDB finds the most similar chunks
7. **Generate** — chunks + question sent to TinyLlama
8. **Answer** — grounded response returned to you

---

## Known Limitations

- TinyLlama is a small model — answers may be verbose or imprecise
- Scanned PDFs without OCR text are not supported
- Maximum file size is 10MB
- Requires Ollama running locally
- Not suitable for production without authentication

---

## Future Improvements

- Add user authentication
- Support larger LLMs (Llama 3, Mistral)
- Add multi-document support
- Deploy to cloud (Railway, Render)
- Add conversation history