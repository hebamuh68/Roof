from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    location: str
    flatmate_pref: Optional[list[str]] = None
    keywords: Optional[list[str]] = None

    class Config:
        orm_model = True