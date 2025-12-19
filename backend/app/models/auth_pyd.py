from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# Response schemas (what server sends back)
class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str
    expires_in: Optional[int] = None  # in seconds

class TokenData(BaseModel):
    email: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str