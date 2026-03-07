from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator('email')
    @classmethod
    def lowercase_email(cls, v):
        return v.lower()


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    phone: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[datetime] = None
    job_title: Optional[str] = None

    @field_validator('first_name', 'last_name')
    @classmethod
    def strip_whitespace(cls, v):
        if not v or not v.strip():
            raise ValueError("This field cannot be empty or only contain whitespace")
        return v.strip()

    @field_validator('email')
    @classmethod
    def lowercase_email(cls, v):
        return v.lower()

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[datetime] = None
    job_title: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[datetime] = None
    job_title: Optional[str] = None

    class Config:
        from_attributes = True
