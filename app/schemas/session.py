from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionBase(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    extracted_email: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    status: Optional[str] = "active"

class SessionCreate(BaseModel):
    user_id: Optional[str] = None
    extracted_email: Optional[str] = None
    ip_address: Optional[str] = None

class SessionInDB(SessionBase):
    pass
