from pydantic import BaseModel, Field
from datetime import datetime

class JobDescriptionIn(BaseModel):
    """Shape of data expected when submitting a job description."""
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=20)

class JobDescriptionOut(BaseModel):
    """Shape of job description data sent back to the client."""
    id: str
    title: str
    description: str
    extracted_skills: list[str]
    created_at: datetime