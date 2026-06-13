from fastapi import HTTPException

MAX_FILE_SIZE_MB = 10
MAX_QUESTION_LENGTH = 500
MIN_QUESTION_LENGTH = 3

def validate_question(question: str) -> str:
    if not question or not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    if len(question.strip()) < MIN_QUESTION_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Question too short. Please ask a proper question."
        )

    if len(question) > MAX_QUESTION_LENGTH:
        question = question[:MAX_QUESTION_LENGTH]

    banned_patterns = ["ignore previous", "forget everything",
                       "you are now", "pretend you are"]
    for pattern in banned_patterns:
        if pattern.lower() in question.lower():
            raise HTTPException(
                status_code=400,
                detail="Invalid question detected."
            )

    return question.strip()

def validate_file_size(file_size: int):
    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE_MB}MB."
        )