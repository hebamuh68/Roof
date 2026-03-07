from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessageCreate(BaseModel):
    receiver_id: str = Field(..., description="Email of the message recipient")
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")


class MessageResponse(BaseModel):
    message_id: int
    sender_id: str
    receiver_id: str
    content: str
    is_read: bool
    created_at: datetime
    sender_name: Optional[str] = None
    receiver_name: Optional[str] = None

    class Config:
        from_attributes = True


class ConversationPreview(BaseModel):
    user_id: str
    user_name: str
    last_message: str
    last_message_time: datetime


class ConversationThread(BaseModel):
    other_user_id: str
    other_user_name: str
    messages: list[MessageResponse]
    total_messages: int
