"""
Pydantic models for Notifications.

These models are used for data validation and serialization/deserialization
of notification-related data.
Models:
    - NotificationCreate: Schema for creating a new notification.
    - NotificationResponse: Schema for notification response.
    - NotificationListResponse: Schema for paginated notification list response.
    - NotificationMarkReadRequest: Schema for marking notifications as read.
"""


from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum


class NotificationCreate(BaseModel):
    """Schema for creating a new notification (internal use)."""
    user_id: int
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class NotificationResponse(BaseModel):
    """Schema for notification response."""
    id: int
    user_id: int
    title: str
    content: Optional[str] = None
    is_read: bool
    data: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Schema for paginated notification list response."""
    notifications: List[NotificationResponse]
    total: int
    unread_count: int
    skip: int
    limit: int


class NotificationMarkReadRequest(BaseModel):
    """Schema for marking notifications as read."""
    notification_ids: Optional[List[int]] = None  # None means mark all as read
