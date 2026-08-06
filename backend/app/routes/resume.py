from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from datetime import datetime, timezone
from pypdf import PdfReader
import io

from app.core.deps import get_current_user
from app.core.database import database

router = APIRouter()
resumes_collection = database["resumes"]


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    # Validate file type — only accept PDFs
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed."
        )

    # Read the uploaded file into memory as bytes
    file_bytes = await file.read()

    # Extract text using pypdf
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        extracted_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not read this PDF. It may be corrupted or image-based."
        )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No extractable text found in this PDF."
        )

    # Save to MongoDB, linked to the logged-in user
    resume_doc = {
        "user_id": current_user["id"],
        "filename": file.filename,
        "extracted_text": extracted_text,
        "uploaded_at": datetime.now(timezone.utc),
    }

    result = await resumes_collection.insert_one(resume_doc)

    return {
        "id": str(result.inserted_id),
        "filename": file.filename,
        "extracted_text": extracted_text,
        "uploaded_at": resume_doc["uploaded_at"],
    }


@router.get("/my-resumes")
async def get_my_resumes(current_user: dict = Depends(get_current_user)):
    """Return all resumes uploaded by the currently logged-in user."""
    cursor = resumes_collection.find({"user_id": current_user["id"]})
    resumes = []
    async for doc in cursor:
        resumes.append({
            "id": str(doc["_id"]),
            "filename": doc["filename"],
            "extracted_text": doc["extracted_text"],
            "uploaded_at": doc["uploaded_at"],
        })
    return resumes