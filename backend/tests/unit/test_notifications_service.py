import pytest
from sqlalchemy.orm import Session
from app.services import notifications_service
from app.schemas.notifications_sql import NotificationDB
from tests.conftest import user_factory


def test_create_notification(db_session: Session):
    """Test creating a notification for a user"""
    user = user_factory(db_session, email="notify_user@test.com")

    notification = notifications_service.create_notification(
        db=db_session,
        user_id=user.id,
        title="Test Notification",
        content="This is a test notification",
        data={"type": "test", "extra_id": 123}
    )

    assert notification.id is not None
    assert notification.user_id == user.id
    assert notification.title == "Test Notification"
    assert notification.content == "This is a test notification"
    assert notification.is_read == False
    assert notification.data["type"] == "test"


def test_create_notification_for_nonexistent_user(db_session: Session):
    """Test that creating notification for non-existent user fails"""
    with pytest.raises(Exception) as exc:
        notifications_service.create_notification(
            db=db_session,
            user_id=99999,
            title="Test"
        )
    assert "User not found" in str(exc.value)


def test_get_user_notifications(db_session: Session):
    """Test getting notifications for a user with pagination"""
    user = user_factory(db_session, email="get_notify@test.com")

    # Create multiple notifications
    for i in range(5):
        notifications_service.create_notification(
            db=db_session,
            user_id=user.id,
            title=f"Notification {i}",
            content=f"Content {i}"
        )

    notifications, total, unread_count = notifications_service.get_user_notifications(
        db=db_session,
        user_id=user.id,
        skip=0,
        limit=10
    )

    assert len(notifications) == 5
    assert total == 5
    assert unread_count == 5


def test_get_user_notifications_pagination(db_session: Session):
    """Test notification pagination"""
    user = user_factory(db_session, email="paginate@test.com")

    for i in range(10):
        notifications_service.create_notification(
            db=db_session,
            user_id=user.id,
            title=f"Notification {i}"
        )

    # Get first page
    notifications, total, _ = notifications_service.get_user_notifications(
        db=db_session,
        user_id=user.id,
        skip=0,
        limit=3
    )

    assert len(notifications) == 3
    assert total == 10


def test_get_unread_only_notifications(db_session: Session):
    """Test filtering for unread notifications only"""
    user = user_factory(db_session, email="unread_only@test.com")

    # Create notifications
    for i in range(3):
        notifications_service.create_notification(
            db=db_session,
            user_id=user.id,
            title=f"Notification {i}"
        )

    # Mark first one as read
    notifications, _, _ = notifications_service.get_user_notifications(
        db=db_session,
        user_id=user.id
    )
    notifications_service.mark_notification_as_read(
        db=db_session,
        notification_id=notifications[0].id,
        user_id=user.id
    )

    # Get unread only
    unread_notifications, total, unread_count = notifications_service.get_user_notifications(
        db=db_session,
        user_id=user.id,
        unread_only=True
    )

    assert len(unread_notifications) == 2
    assert unread_count == 2


def test_mark_notification_as_read(db_session: Session):
    """Test marking a single notification as read"""
    user = user_factory(db_session, email="mark_read@test.com")

    notification = notifications_service.create_notification(
        db=db_session,
        user_id=user.id,
        title="Test"
    )

    assert notification.is_read == False

    updated = notifications_service.mark_notification_as_read(
        db=db_session,
        notification_id=notification.id,
        user_id=user.id
    )

    assert updated.is_read == True


def test_mark_notification_unauthorized(db_session: Session):
    """Test that user cannot mark another user's notification as read"""
    user1 = user_factory(db_session, email="owner@test.com")
    user2 = user_factory(db_session, email="other@test.com")

    notification = notifications_service.create_notification(
        db=db_session,
        user_id=user1.id,
        title="Test"
    )

    with pytest.raises(Exception) as exc:
        notifications_service.mark_notification_as_read(
            db=db_session,
            notification_id=notification.id,
            user_id=user2.id
        )
    assert "Not authorized" in str(exc.value)


def test_mark_all_notifications_as_read(db_session: Session):
    """Test marking all notifications as read"""
    user = user_factory(db_session, email="mark_all@test.com")

    for i in range(5):
        notifications_service.create_notification(
            db=db_session,
            user_id=user.id,
            title=f"Notification {i}"
        )

    count = notifications_service.mark_notifications_as_read(
        db=db_session,
        user_id=user.id
    )

    assert count == 5

    # Verify all are read
    unread = notifications_service.get_unread_count(db_session, user.id)
    assert unread == 0


def test_delete_notification(db_session: Session):
    """Test deleting a notification"""
    user = user_factory(db_session, email="delete_notify@test.com")

    notification = notifications_service.create_notification(
        db=db_session,
        user_id=user.id,
        title="To Delete"
    )
    notification_id = notification.id

    result = notifications_service.delete_notification(
        db=db_session,
        notification_id=notification_id,
        user_id=user.id
    )

    assert result == True

    # Verify it's gone
    with pytest.raises(Exception) as exc:
        notifications_service.get_notification_by_id(
            db=db_session,
            notification_id=notification_id,
            user_id=user.id
        )
    assert "not found" in str(exc.value)


def test_delete_all_notifications(db_session: Session):
    """Test deleting all notifications for a user"""
    user = user_factory(db_session, email="delete_all@test.com")

    for i in range(5):
        notifications_service.create_notification(
            db=db_session,
            user_id=user.id,
            title=f"Notification {i}"
        )

    count = notifications_service.delete_all_notifications(
        db=db_session,
        user_id=user.id
    )

    assert count == 5

    # Verify all are gone
    notifications, total, _ = notifications_service.get_user_notifications(
        db=db_session,
        user_id=user.id
    )
    assert total == 0


def test_get_unread_count(db_session: Session):
    """Test getting unread notification count"""
    user = user_factory(db_session, email="count@test.com")

    for i in range(3):
        notifications_service.create_notification(
            db=db_session,
            user_id=user.id,
            title=f"Notification {i}"
        )

    count = notifications_service.get_unread_count(db_session, user.id)
    assert count == 3


def test_notify_new_message(db_session: Session):
    """Test creating notification for new message"""
    receiver = user_factory(db_session, email="msg_receiver@test.com")

    notification = notifications_service.notify_new_message(
        db=db_session,
        receiver_id=receiver.id,
        sender_id=999,
        sender_name="John Doe",
        message_preview="Hello, I'm interested in your apartment!",
        message_id=123
    )

    assert notification.user_id == receiver.id
    assert "John Doe" in notification.title
    assert notification.data["type"] == "new_message"
    assert notification.data["sender_id"] == 999
    assert notification.data["message_id"] == 123


def test_notify_new_message_truncates_long_content(db_session: Session):
    """Test that long message previews are truncated"""
    receiver = user_factory(db_session, email="truncate@test.com")

    long_message = "A" * 200  # More than 100 chars

    notification = notifications_service.notify_new_message(
        db=db_session,
        receiver_id=receiver.id,
        sender_id=999,
        sender_name="Test User",
        message_preview=long_message,
        message_id=1
    )

    assert len(notification.content) == 100
    assert notification.content.endswith("...")


def test_message_creates_notification(db_session: Session):
    """Test that sending a message creates a notification for receiver"""
    from app.services import message_service
    from app.models.message_pyd import MessageCreate

    sender = user_factory(db_session, email="msg_sender@test.com")
    receiver = user_factory(db_session, email="msg_receiver2@test.com")

    message_data = MessageCreate(
        receiver_id=receiver.id,
        content="Hello from sender!"
    )

    message_service.send_message(db_session, sender.id, message_data)

    # Check notification was created
    notifications, total, _ = notifications_service.get_user_notifications(
        db=db_session,
        user_id=receiver.id
    )

    assert total == 1
    assert "message" in notifications[0].title.lower()
    assert notifications[0].data["message_id"] is not None
