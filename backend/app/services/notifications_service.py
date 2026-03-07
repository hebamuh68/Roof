from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from app.schemas.notifications_sql import NotificationDB
from app.schemas.user_sql import UserDB


def create_notification(
    db: Session,
    sender_email: str,
    receiver_email: str,
    title: str,
    content: Optional[str] = None,
    type: Optional[str] = None,
) -> NotificationDB:
    receiver = db.query(UserDB).filter(UserDB.email == receiver_email).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    notification = NotificationDB(
        sender_id=sender_email,
        receiver_id=receiver_email,
        title=title,
        content=content,
        type=type,
        is_read=False,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_user_notifications(
    db: Session,
    user_email: str,
    skip: int = 0,
    limit: int = 50,
    unread_only: bool = False,
) -> tuple[List[NotificationDB], int, int]:
    query = db.query(NotificationDB).filter(NotificationDB.receiver_id == user_email)

    if unread_only:
        query = query.filter(NotificationDB.is_read == False)

    total = query.count()

    unread_count = db.query(NotificationDB).filter(
        NotificationDB.receiver_id == user_email,
        NotificationDB.is_read == False,
    ).count()

    notifications = query.order_by(
        desc(NotificationDB.created_at)
    ).offset(skip).limit(limit).all()

    return notifications, total, unread_count


def get_notification_by_id(
    db: Session,
    notification_id: int,
    user_email: str,
) -> NotificationDB:
    notification = db.query(NotificationDB).filter(
        NotificationDB.notification_id == notification_id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    if notification.receiver_id != user_email:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this notification"
        )

    return notification


def mark_notification_as_read(
    db: Session,
    notification_id: int,
    user_email: str,
) -> NotificationDB:
    notification = get_notification_by_id(db, notification_id, user_email)
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification


def mark_notifications_as_read(
    db: Session,
    user_email: str,
    notification_ids: Optional[List[int]] = None,
) -> int:
    query = db.query(NotificationDB).filter(
        NotificationDB.receiver_id == user_email,
        NotificationDB.is_read == False,
    )

    if notification_ids:
        query = query.filter(NotificationDB.notification_id.in_(notification_ids))

    count = query.update({"is_read": True}, synchronize_session=False)
    db.commit()
    return count


def delete_notification(
    db: Session,
    notification_id: int,
    user_email: str,
) -> bool:
    notification = get_notification_by_id(db, notification_id, user_email)
    db.delete(notification)
    db.commit()
    return True


def delete_all_notifications(
    db: Session,
    user_email: str,
    read_only: bool = False,
) -> int:
    query = db.query(NotificationDB).filter(
        NotificationDB.receiver_id == user_email
    )

    if read_only:
        query = query.filter(NotificationDB.is_read == True)

    count = query.delete(synchronize_session=False)
    db.commit()
    return count


def get_unread_count(db: Session, user_email: str) -> int:
    return db.query(NotificationDB).filter(
        NotificationDB.receiver_id == user_email,
        NotificationDB.is_read == False,
    ).count()


def notify_new_message(
    db: Session,
    receiver_email: str,
    sender_email: str,
    sender_name: str,
    message_preview: str,
    message_id: int,
) -> NotificationDB:
    if len(message_preview) > 100:
        message_preview = message_preview[:97] + "..."

    return create_notification(
        db=db,
        sender_email=sender_email,
        receiver_email=receiver_email,
        title=f"New message from {sender_name}",
        content=message_preview,
        type="new_message",
    )


def notify_property_inquiry(
    db: Session,
    owner_email: str,
    inquirer_email: str,
    inquirer_name: str,
    property_title: str,
) -> NotificationDB:
    return create_notification(
        db=db,
        sender_email=inquirer_email,
        receiver_email=owner_email,
        title=f"New inquiry about {property_title}",
        content=f"{inquirer_name} is interested in your listing",
        type="property_inquiry",
    )
