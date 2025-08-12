from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(..., pattern=r'^\S+@\S+\.\S+$')
    location: str
    flatmate_pref: Optional[list] = None
    keywords: Optional[list] = None

    class Config:
        orm_model = True
    
