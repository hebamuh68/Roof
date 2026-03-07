from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class NotificationCreate(BaseModel):
    receiver_id: str
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None
    type: Optional[str] = None


class NotificationResponse(BaseModel):
    notification_id: int
    sender_id: str
    receiver_id: str
    title: str
    content: Optional[str] = None
    type: Optional[str] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]
    total: int
    unread_count: int
    skip: int
    limit: int


class NotificationMarkReadRequest(BaseModel):
    notification_ids: Optional[List[int]] = None
