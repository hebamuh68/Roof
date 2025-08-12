from pydantic import BaseModel
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