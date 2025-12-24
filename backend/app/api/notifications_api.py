from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.schemas.user_sql import UserDB
from app.models.notifications_pyd import (
    NotificationResponse,
    NotificationListResponse,
    NotificationMarkReadRequest,
)
from app.services import notifications_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=NotificationListResponse)
def get_notifications(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=50, ge=1, le=100, description="Max records to return"),
    unread_only: bool = Query(default=False, description="Only return unread notifications"),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Get all notifications for the current user with pagination.

    Returns notifications sorted by creation date (newest first).
    """
    notifications, total, unread_count = notifications_service.get_user_notifications(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        unread_only=unread_only
    )

    return NotificationListResponse(
        notifications=[
            NotificationResponse.model_validate(n) for n in notifications
        ],
        total=total,
        unread_count=unread_count,
        skip=skip,
        limit=limit
    )


@router.get("/unread-count", response_model=dict)
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Get the count of unread notifications for the current user.

    Useful for displaying notification badges.
    """
    count = notifications_service.get_unread_count(db, current_user.id)
    return {"unread_count": count}


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Get a single notification by ID.

    Only accessible by the notification's target user.
    """
    notification = notifications_service.get_notification_by_id(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )
    return NotificationResponse.model_validate(notification)


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Mark a single notification as read.
    """
    notification = notifications_service.mark_notification_as_read(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )
    return NotificationResponse.model_validate(notification)


@router.patch("/mark-read", response_model=dict)
def mark_notifications_read(
    request: NotificationMarkReadRequest,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Mark multiple notifications as read.

    If notification_ids is not provided, marks ALL notifications as read.
    """
    count = notifications_service.mark_notifications_as_read(
        db=db,
        user_id=current_user.id,
        notification_ids=request.notification_ids
    )
    return {"message": f"Marked {count} notifications as read", "count": count}


@router.delete("/{notification_id}", response_model=dict)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Delete a single notification.

    Only accessible by the notification's target user.
    """
    notifications_service.delete_notification(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )
    return {"message": "Notification deleted successfully"}


@router.delete("/", response_model=dict)
def delete_all_notifications(
    read_only: bool = Query(
        default=False,
        description="If true, only delete read notifications"
    ),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Delete all notifications for the current user.

    Optionally only delete read notifications to preserve unread ones.
    """
    count = notifications_service.delete_all_notifications(
        db=db,
        user_id=current_user.id,
        read_only=read_only
    )
    return {"message": f"Deleted {count} notifications", "count": count}
