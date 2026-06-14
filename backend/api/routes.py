from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from backend.core.document_reader import read_document
from backend.core.text_chunker import chunk_document
from backend.core.vector_store import store_chunks, search_chunks
from backend.agents.rag_agent import decide_and_answer
from backend.utils.validator import validate_question, validate_file_size
from backend.utils.error_handler import (check_groq_running,
                                          safe_generate,
                                          add_confidence_warning)
import os, shutil

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".csv", ".xlsx"}

class QuestionRequest(BaseModel):
    question: str
    filename: str

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Safety 1 — check file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Use: {ALLOWED_EXTENSIONS}"
        )

    # Safety 2 — check file size
    contents = await file.read()
    validate_file_size(len(contents))

    # Save file
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        f.write(contents)

    # Safety 3 — check if document is readable
    try:
        text = read_document(save_path)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Could not read document: {str(e)}"
        )

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="Document appears to be empty or unreadable."
        )

    chunks = chunk_document(text, file.filename)
    stored = store_chunks(chunks, file.filename)

    word_count = len(text.split())
    preview = text[:300]

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "type": ext,
        "word_count": word_count,
        "chunk_count": len(chunks),
        "vectors_stored": stored,
        "preview": preview,
        "chunks": chunks
    }

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    # Safety 4 — validate question
    question = validate_question(request.question)

    # Safety 5 — check Groq is running
    if not check_groq_running():
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Groq API. Check your GROQ_API_KEY in .env"
        )

    # Retrieve relevant chunks
    relevant_chunks = search_chunks(
        query=question,
        filename=request.filename,
        top_k=3
    )

    # Safety 6 — safe generate with error handling
    result = safe_generate(decide_and_answer, question, relevant_chunks)

    if isinstance(result, str):
        return {
            "question": question,
            "answer": result,
            "tool_used": "error",
            "reasoning": "An error occurred during generation.",
            "filename": request.filename,
            "relevant_chunks": []
        }

    # Safety 7 — add confidence warning if needed
    answer = add_confidence_warning(result["answer"], relevant_chunks)

    return {
        "question": question,
        "answer": answer,
        "tool_used": result["tool_used"],
        "reasoning": result["reasoning"],
        "filename": request.filename,
        "relevant_chunks": relevant_chunks
    }

@router.get("/files")
async def list_files():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}