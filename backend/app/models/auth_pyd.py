from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# Request schemas (what client sends)
class UserCreate(BaseModel):
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

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Response schemas (what server sends back)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None