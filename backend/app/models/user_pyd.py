from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    location: str
    flatmate_pref: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    password: str
    role: str = "seeker"
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    location: str
    flatmate_pref: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    role: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    location: Optional[str] = None
    flatmate_pref: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    password: Optional[str] = None
    role: Optional[str] = "seeker"

    class Config:
        from_attributes = True