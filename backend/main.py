from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from backend.api.routes import router

app = FastAPI(
    title=os.getenv("APP_NAME", "ReleaseNote Chatbot"),
    description="Ask questions to your documents using AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "ReleaseNote Chatbot API is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "app": os.getenv("APP_NAME")}