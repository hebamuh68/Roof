from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Apartment(BaseModel):
    title: str
    description: str
    location: str
    apartment_type: str
    rent_per_week: int
    start_date: datetime
    duration_len: Optional[int] = None
    place_accept: str
    furnishing_type: str
    is_pathroom_solo: bool = False
    parking_type: str
    keywords: Optional[list] = None
    is_active: bool = True

    class Config:
        orm_model = True

class FilterApartment(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    apartment_type: Optional[str] = None
    rent_per_week: Optional[int] = None
    start_date: Optional[datetime] = None
    duration_len: Optional[int] = None
    place_accept: Optional[str] = None
    furnishing_type: Optional[str] = None
    is_pathroom_solo: Optional[bool] = None
    parking_type: Optional[str] = None
    keywords: Optional[list] = None
    is_active: Optional[bool] = None

    class Config:
        orm_model = True