from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, List
from datetime import datetime

# Auth schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str


    @field_validator('email')
    @classmethod
    def lowercase_email(cls, v):
        return v.lower()

# User schemas
class UserData(BaseModel):
    id: Optional[int] = None
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    location: str = Field(..., min_length=2, max_length=50)
    flatmate_pref: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    role: str = Field(default="seeker", pattern=r"^(seeker|renter)$")
    created_at: Optional[datetime] = None

    @field_validator('first_name', 'last_name', 'location')
    @classmethod
    def strip_whitespace(cls, v):
        if not v or not v.strip():
            raise ValueError("This field cannot be empty or only contain whitespace")
        return v.strip()

    @field_validator('email')
    @classmethod
    def lowercase_email(cls, v):
        return v.lower()

    @field_validator('flatmate_pref', 'keywords')
    @classmethod
    def validate_lists(cls, v):
        if v is None:
            return []
        return [item.strip() for item in v if item and item.strip()]

    @field_validator('role')
    @classmethod
    def lowercase_role(cls, v):
        return v.lower()

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