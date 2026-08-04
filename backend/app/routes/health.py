from fastapi import APIRouter
from app.core.database import database

router = APIRouter()

@router.get("/health")
async def health_check():
    try:
        # The ping command is the cheapest way to verify a live DB connection
        await database.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "ok",
        "message": "SkillMatch backend is running",
        "database": db_status
    }