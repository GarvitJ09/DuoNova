from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class ResumeBase(BaseModel):
    resume_id: str
    session_id: str
    user_id: Optional[str] = None
    file_name: str
    file_path: str
    file_size: int
    raw_text: str
    json_data: Dict
    extraction_confidence: float
    created_at: Optional[datetime] = None
    level: str  # New field for job level
    job_description: Optional[str] = None  # Job description field

class ResumeCreate(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    file_name: str
    file_path: str
    file_size: int
    raw_text: str
    json_data: Dict
    extraction_confidence: float
    level: str  # New field for job level
    job_description: Optional[str] = None  # Job description field

class ResumeInDB(ResumeBase):
    pass
