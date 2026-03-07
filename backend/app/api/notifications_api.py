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
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    unread_only: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    notifications, total, unread_count = notifications_service.get_user_notifications(
        db=db, user_email=current_user.email, skip=skip, limit=limit, unread_only=unread_only
    )
    return NotificationListResponse(
        notifications=[NotificationResponse.model_validate(n) for n in notifications],
        total=total,
        unread_count=unread_count,
        skip=skip,
        limit=limit,
    )


@router.get("/unread-count", response_model=dict)
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    count = notifications_service.get_unread_count(db, current_user.email)
    return {"unread_count": count}


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    notification = notifications_service.get_notification_by_id(
        db=db, notification_id=notification_id, user_email=current_user.email
    )
    return NotificationResponse.model_validate(notification)


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    notification = notifications_service.mark_notification_as_read(
        db=db, notification_id=notification_id, user_email=current_user.email
    )
    return NotificationResponse.model_validate(notification)


@router.patch("/mark-read", response_model=dict)
def mark_notifications_read(
    request: NotificationMarkReadRequest,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    count = notifications_service.mark_notifications_as_read(
        db=db, user_email=current_user.email, notification_ids=request.notification_ids
    )
    return {"message": f"Marked {count} notifications as read", "count": count}


@router.delete("/{notification_id}", response_model=dict)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    notifications_service.delete_notification(
        db=db, notification_id=notification_id, user_email=current_user.email
    )
    return {"message": "Notification deleted successfully"}


@router.delete("/", response_model=dict)
def delete_all_notifications(
    read_only: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    count = notifications_service.delete_all_notifications(
        db=db, user_email=current_user.email, read_only=read_only
    )
    return {"message": f"Deleted {count} notifications", "count": count}
