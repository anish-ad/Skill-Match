from pydantic import BaseModel
from datetime import datetime

class ResumeOut(BaseModel):
    """Shape of resume data we send back to the client."""
    id: str
    filename: str
    extracted_text: str
    uploaded_at: datetime