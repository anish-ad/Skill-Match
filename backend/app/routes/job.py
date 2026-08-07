from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId

from app.models.job import JobDescriptionIn
from app.core.deps import get_current_user
from app.core.database import database
from app.core.skill_extractor import extract_skills

router = APIRouter()
jobs_collection = database["job_descriptions"]


@router.post("/analyze")
async def analyze_job_description(
    job: JobDescriptionIn,
    current_user: dict = Depends(get_current_user)
):
    # Run our skill extraction on the submitted description
    skills = extract_skills(job.description)

    job_doc = {
        "user_id": current_user["id"],
        "title": job.title,
        "description": job.description,
        "extracted_skills": skills,
        "created_at": datetime.now(timezone.utc),
    }

    result = await jobs_collection.insert_one(job_doc)

    return {
        "id": str(result.inserted_id),
        "title": job.title,
        "description": job.description,
        "extracted_skills": skills,
        "created_at": job_doc["created_at"],
    }


@router.get("/my-jobs")
async def get_my_jobs(current_user: dict = Depends(get_current_user)):
    """Return all job descriptions the current user has analyzed."""
    cursor = jobs_collection.find({"user_id": current_user["id"]})
    jobs = []
    async for doc in cursor:
        jobs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "description": doc["description"],
            "extracted_skills": doc["extracted_skills"],
            "created_at": doc["created_at"],
        })
    return jobs