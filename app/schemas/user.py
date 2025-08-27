from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    user_id: str
    primary_email: EmailStr
    alternate_emails: List[EmailStr] = []
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    name: Optional[str] = None
    verification_status: Optional[str] = "pending"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserCreate(BaseModel):
    primary_email: EmailStr
    alternate_emails: List[EmailStr] = []
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    name: Optional[str] = None

class UserInDB(UserBase):
    pass
