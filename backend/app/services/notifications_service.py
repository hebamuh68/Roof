from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from app.schemas.notifications_sql import NotificationDB
from app.schemas.user_sql import UserDB


def create_notification(
    db: Session,
    user_id: int,
    title: str,
    content: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None
) -> NotificationDB:
    """
    Create a new notification for a user.

    Args:
        db: Database session
        user_id: Target user ID
        title: Notification title
        content: Optional detailed content
        data: Optional JSON data with related entity IDs

    Returns:
        Created notification object
    """
    # Verify user exists
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    notification = NotificationDB(
        user_id=user_id,
        title=title,
        content=content,
        data=data,
        is_read=False,
        created_at=datetime.now(timezone.utc)
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


def get_user_notifications(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    unread_only: bool = False
) -> tuple[List[NotificationDB], int, int]:
    """
    Get notifications for a user with pagination.

    Args:
        db: Database session
        user_id: User ID to get notifications for
        skip: Number of records to skip
        limit: Maximum number of records to return
        unread_only: If True, only return unread notifications

    Returns:
        Tuple of (notifications list, total count, unread count)
    """
    query = db.query(NotificationDB).filter(NotificationDB.user_id == user_id)

    if unread_only:
        query = query.filter(NotificationDB.is_read == False)

    # Get total count
    total = query.count()

    # Get unread count
    unread_count = db.query(NotificationDB).filter(
        NotificationDB.user_id == user_id,
        NotificationDB.is_read == False
    ).count()

    # Get paginated results
    notifications = query.order_by(
        desc(NotificationDB.created_at)
    ).offset(skip).limit(limit).all()

    return notifications, total, unread_count


def get_notification_by_id(
    db: Session,
    notification_id: int,
    user_id: int
) -> NotificationDB:
    """
    Get a single notification by ID, verifying ownership.

    Args:
        db: Database session
        notification_id: Notification ID
        user_id: User ID for ownership verification

    Returns:
        Notification object

    Raises:
        HTTPException: If notification not found or user doesn't own it
    """
    notification = db.query(NotificationDB).filter(
        NotificationDB.id == notification_id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    if notification.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this notification"
        )

    return notification


def mark_notification_as_read(
    db: Session,
    notification_id: int,
    user_id: int
) -> NotificationDB:
    """
    Mark a single notification as read.

    Args:
        db: Database session
        notification_id: Notification ID to mark as read
        user_id: User ID for ownership verification

    Returns:
        Updated notification object
    """
    notification = get_notification_by_id(db, notification_id, user_id)
    notification.is_read = True
    db.commit()
    db.refresh(notification)

    return notification


def mark_notifications_as_read(
    db: Session,
    user_id: int,
    notification_ids: Optional[List[int]] = None
) -> int:
    """
    Mark multiple notifications as read.

    Args:
        db: Database session
        user_id: User ID for ownership verification
        notification_ids: List of notification IDs to mark as read.
                         If None, marks all user's notifications as read.

    Returns:
        Number of notifications updated
    """
    query = db.query(NotificationDB).filter(
        NotificationDB.user_id == user_id,
        NotificationDB.is_read == False
    )

    if notification_ids:
        query = query.filter(NotificationDB.id.in_(notification_ids))

    count = query.update({"is_read": True}, synchronize_session=False)
    db.commit()

    return count


def delete_notification(
    db: Session,
    notification_id: int,
    user_id: int
) -> bool:
    """
    Delete a notification.

    Args:
        db: Database session
        notification_id: Notification ID to delete
        user_id: User ID for ownership verification

    Returns:
        True if deleted successfully
    """
    notification = get_notification_by_id(db, notification_id, user_id)
    db.delete(notification)
    db.commit()

    return True


def delete_all_notifications(
    db: Session,
    user_id: int,
    read_only: bool = False
) -> int:
    """
    Delete all notifications for a user.

    Args:
        db: Database session
        user_id: User ID
        read_only: If True, only delete read notifications

    Returns:
        Number of notifications deleted
    """
    query = db.query(NotificationDB).filter(
        NotificationDB.user_id == user_id
    )

    if read_only:
        query = query.filter(NotificationDB.is_read == True)

    count = query.delete(synchronize_session=False)
    db.commit()

    return count


def get_unread_count(db: Session, user_id: int) -> int:
    """
    Get the count of unread notifications for a user.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        Count of unread notifications
    """
    return db.query(NotificationDB).filter(
        NotificationDB.user_id == user_id,
        NotificationDB.is_read == False
    ).count()


# =============================================================================
# Notification Trigger Functions (called by other services)
# =============================================================================

def notify_new_message(
    db: Session,
    receiver_id: int,
    sender_id: int,
    sender_name: str,
    message_preview: str,
    message_id: int
) -> NotificationDB:
    """
    Create a notification for a new message received.

    Args:
        db: Database session
        receiver_id: ID of the user receiving the message
        sender_id: ID of the message sender
        sender_name: Name of the sender for display
        message_preview: Truncated message content
        message_id: ID of the message

    Returns:
        Created notification object
    """
    # Truncate message preview
    if len(message_preview) > 100:
        message_preview = message_preview[:97] + "..."

    return create_notification(
        db=db,
        user_id=receiver_id,
        title=f"New message from {sender_name}",
        content=message_preview,
        data={
            "type": "new_message",
            "sender_id": sender_id,
            "message_id": message_id
        }
    )


def notify_apartment_inquiry(
    db: Session,
    owner_id: int,
    inquirer_name: str,
    apartment_title: str,
    apartment_id: int,
    message_id: int
) -> NotificationDB:
    """
    Create a notification for an apartment inquiry.

    Args:
        db: Database session
        owner_id: ID of the apartment owner
        inquirer_name: Name of the person making the inquiry
        apartment_title: Title of the apartment
        apartment_id: ID of the apartment
        message_id: ID of the inquiry message

    Returns:
        Created notification object
    """
    return create_notification(
        db=db,
        user_id=owner_id,
        title=f"New inquiry about {apartment_title}",
        content=f"{inquirer_name} is interested in your listing",
        data={
            "type": "apartment_inquiry",
            "apartment_id": apartment_id,
            "message_id": message_id,
            "inquirer_name": inquirer_name
        }
    )
