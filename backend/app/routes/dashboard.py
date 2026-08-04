from fastapi import APIRouter, Depends
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    """A protected route — only accessible with a valid JWT."""
    return {
        "message": f"Welcome back, {current_user['name']}!",
        "user": current_user
    }