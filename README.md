# 📄 ReleaseNote Chatbot

A Retrieval-Augmented Generation (RAG) system that lets you upload 
enterprise documents and ask natural language questions about them.

---

## What it does

Upload any PDF, TXT, CSV, or Excel file and ask questions in plain English.
The app finds the most relevant parts of your document and generates
accurate, grounded answers using Groq's Llama 3.3 70B model.

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
        rag_pipeline     ← generates answer using Groq LLM
                ↓
           ChromaDB (local vector database)
                ↓
           Groq API (llama-3.3-70b-versatile)

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Frontend | Streamlit | User interface |
| Backend | FastAPI | API server |
| Embeddings | sentence-transformers | Free local embeddings |
| Vector DB | ChromaDB | Semantic search |
| LLM | Groq (Llama 3.3 70B) | Answer generation |
| Deployment | Docker + Docker Compose | Containerized deployment |

---

## Project Structure

    releaseNoteChatbot/
    ├── app.py                  ← Streamlit UI
    ├── Dockerfile.backend      ← Docker config for FastAPI
    ├── Dockerfile.frontend     ← Docker config for Streamlit
    ├── docker-compose.yml      ← Orchestrates both containers
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
    ├── chroma_db/              ← Vector database (auto-created)
    ├── uploaded_files/         ← Uploaded documents (auto-created)
    ├── requirements.txt
    └── .env

---

## How to Run with Docker (Recommended)

**1. Clone the repository**

    git clone https://github.com/lekhanairk2006/releaseNoteChatbot.git
    cd releaseNoteChatbot

**2. Set up environment variables**

    cp .env.example .env

Edit `.env` and add your Groq API key:

    GROQ_API_KEY=your_groq_key_here
    APP_NAME=ReleaseNote Chatbot
    DEBUG=True

**3. Start the app**

    docker-compose up

**4. Open the app**

Go to http://localhost:8501

**5. Stop the app**

    docker-compose down

---

## How to Run Locally (Without Docker)

**1. Clone the repository**

    git clone https://github.com/lekhanairk2006/releaseNoteChatbot.git
    cd releaseNoteChatbot

**2. Create virtual environment**

    python -m venv venv
    source venv/bin/activate

**3. Install dependencies**

    pip install -r requirements.txt
    pip install sentence-transformers groq

**4. Set up environment variables**

    cp .env.example .env

Edit `.env` and add your Groq API key.

**5. Start FastAPI backend**

    uvicorn backend.main:app --reload

**6. Start Streamlit frontend (new terminal)**

    streamlit run app.py

**7. Open the app**

Go to http://localhost:8501

---

## How RAG Works

1. **Upload** — document is saved and text is extracted
2. **Chunk** — text is split into 200-word overlapping pieces
3. **Embed** — each chunk is converted to 384 numbers (vectors)
4. **Store** — vectors saved in ChromaDB
5. **Query** — your question is also converted to a vector
6. **Search** — ChromaDB finds the most similar chunks
7. **Generate** — chunks + question sent to Groq LLM
8. **Answer** — grounded response returned to you

---

## How the Agent Works

The app uses an AI agent that decides how to answer each question:

- **Document Search** — used for questions about the uploaded document
- **Direct Answer** — used for general knowledge questions

The agent shows which tool it used and its reasoning for every response.

---

## Known Limitations

- Maximum file size is 10MB
- Requires a Groq API key (free at console.groq.com)
- ChromaDB data is stored locally and resets if Docker volumes are removed
- Not suitable for production without authentication

---

## Future Improvements

- Add user authentication
- Add conversation history
