from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Request model for sending a message
class MessageCreate(BaseModel):
    receiver_id: int = Field(..., description="ID of the message recipient")
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")


# Response model for a message
class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
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


# Response model for a conversation thread
class ConversationThread(BaseModel):
    other_user_id: int
    other_user_name: str
    messages: list[MessageResponse]
    total_messages: int