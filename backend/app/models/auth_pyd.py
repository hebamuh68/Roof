from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# Response schemas (what server sends back)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None