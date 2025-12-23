from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Request model for sending a message
class MessageCreate(BaseModel):
    receiver_id: int = Field(..., description="ID of the message recipient")
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")
    apartment_id: Optional[int] = Field(None, description="Optional apartment ID if discussing a listing")


# Request model for marking as read
class MessageMarkRead(BaseModel):
    message_ids: list[int] = Field(..., description="List of message IDs to mark as read")


# Response model for a message
class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    apartment_id: Optional[int]
    is_read: bool
    read_at: Optional[datetime]
    created_at: datetime

    # Optional: Include sender/receiver names
    sender_name: Optional[str] = None
    receiver_name: Optional[str] = None

    class Config:
        from_attributes = True


# Response model for a conversation preview
class ConversationPreview(BaseModel):
    user_id: int  # The other user in the conversation
    user_name: str
    last_message: str
    last_message_time: datetime
    unread_count: int
    apartment_id: Optional[int] = None


# Response model for a conversation thread
class ConversationThread(BaseModel):
    other_user_id: int
    other_user_name: str
    messages: list[MessageResponse]
    total_messages: int