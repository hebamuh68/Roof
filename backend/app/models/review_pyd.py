from pydantic import BaseModel, Field
from typing import Optional


class ReviewCreate(BaseModel):
    property_id: int
    content: Optional[str] = None
    stars: int = Field(..., ge=1, le=5)


class ReviewResponse(BaseModel):
    review_id: int
    user_id: str
    property_id: int
    content: Optional[str] = None
    stars: int

    class Config:
        from_attributes = True
