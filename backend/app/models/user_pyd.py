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
