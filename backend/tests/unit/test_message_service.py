import pytest
from sqlalchemy.orm import Session
from app.services import message_service
from app.models.message_pyd import MessageCreate
from tests.conftest import user_factory


def test_send_message(db_session: Session):
    """Test sending a message between users"""
    sender = user_factory(db_session, email="sender@test.com")
    receiver = user_factory(db_session, email="receiver@test.com")

    message_data = MessageCreate(
        receiver_id=receiver.id,
        content="Hello, this is a test message"
    )

    message = message_service.send_message(db_session, sender.id, message_data)

    assert message.sender_id == sender.id
    assert message.receiver_id == receiver.id
    assert message.content == "Hello, this is a test message"
    assert message.is_read == False
    assert message.apartment_id is None


def test_send_message_with_apartment(db_session: Session):
    """Test sending a message with apartment context"""
    from tests.conftest import apartment_factory

    sender = user_factory(db_session, email="sender2@test.com")
    receiver = user_factory(db_session, email="receiver2@test.com")
    apartment = apartment_factory(db_session, renter_id=receiver.id)

    message_data = MessageCreate(
        receiver_id=receiver.id,
        content="I'm interested in your apartment!",
        apartment_id=apartment.id
    )

    message = message_service.send_message(db_session, sender.id, message_data)

    assert message.apartment_id == apartment.id


def test_get_conversations(db_session: Session):
    """Test retrieving user conversations"""
    user1 = user_factory(db_session, email="user1@test.com")
    user2 = user_factory(db_session, email="user2@test.com")

    # Send messages
    msg1 = MessageCreate(receiver_id=user2.id, content="Message 1")
    message_service.send_message(db_session, user1.id, msg1)

    # Get conversations for user1
    conversations = message_service.get_conversations(db_session, user1.id)

    assert len(conversations) == 1
    assert conversations[0].user_id == user2.id
    assert conversations[0].unread_count == 0  # user1 sent the message


def test_get_conversations_with_unread(db_session: Session):
    """Test conversations show correct unread count"""
    user1 = user_factory(db_session, email="user3@test.com")
    user2 = user_factory(db_session, email="user4@test.com")

    # user2 sends messages to user1
    msg1 = MessageCreate(receiver_id=user1.id, content="Message 1")
    msg2 = MessageCreate(receiver_id=user1.id, content="Message 2")
    message_service.send_message(db_session, user2.id, msg1)
    message_service.send_message(db_session, user2.id, msg2)

    # Get conversations for user1 (receiver)
    conversations = message_service.get_conversations(db_session, user1.id)

    assert len(conversations) == 1
    assert conversations[0].unread_count == 2


def test_mark_messages_as_read(db_session: Session):
    """Test marking messages as read"""
    sender = user_factory(db_session, email="sender3@test.com")
    receiver = user_factory(db_session, email="receiver3@test.com")

    # Send message
    msg_data = MessageCreate(receiver_id=receiver.id, content="Test message")
    message = message_service.send_message(db_session, sender.id, msg_data)

    # Mark as read
    updated = message_service.mark_messages_as_read(
        db_session,
        receiver.id,
        [message.id]
    )

    assert updated == 1

    # Verify it's marked as read
    db_session.refresh(message)
    assert message.is_read == True
    assert message.read_at is not None


def test_mark_messages_as_read_sender_cannot_mark(db_session: Session):
    """Test that sender cannot mark their own sent message as read"""
    sender = user_factory(db_session, email="sender4@test.com")
    receiver = user_factory(db_session, email="receiver4@test.com")

    msg_data = MessageCreate(receiver_id=receiver.id, content="Test message")
    message = message_service.send_message(db_session, sender.id, msg_data)

    # Sender tries to mark as read (should fail)
    updated = message_service.mark_messages_as_read(
        db_session,
        sender.id,
        [message.id]
    )

    assert updated == 0


def test_get_unread_count(db_session: Session):
    """Test getting unread message count"""
    user1 = user_factory(db_session, email="user5@test.com")
    user2 = user_factory(db_session, email="user6@test.com")

    # Initially no unread messages
    count = message_service.get_unread_count(db_session, user1.id)
    assert count == 0

    # user2 sends messages to user1
    msg1 = MessageCreate(receiver_id=user1.id, content="Message 1")
    msg2 = MessageCreate(receiver_id=user1.id, content="Message 2")
    message_service.send_message(db_session, user2.id, msg1)
    message_service.send_message(db_session, user2.id, msg2)

    # Check unread count
    count = message_service.get_unread_count(db_session, user1.id)
    assert count == 2


def test_get_conversation_thread(db_session: Session):
    """Test getting full conversation thread"""
    user1 = user_factory(db_session, email="user7@test.com")
    user2 = user_factory(db_session, email="user8@test.com")

    # Exchange messages
    msg1 = MessageCreate(receiver_id=user2.id, content="Hello!")
    msg2 = MessageCreate(receiver_id=user1.id, content="Hi there!")
    msg3 = MessageCreate(receiver_id=user2.id, content="How are you?")

    message_service.send_message(db_session, user1.id, msg1)
    message_service.send_message(db_session, user2.id, msg2)
    message_service.send_message(db_session, user1.id, msg3)

    # Get conversation thread
    thread = message_service.get_conversation_thread(db_session, user1.id, user2.id)

    assert thread["total_messages"] == 3
    assert len(thread["messages"]) == 3
    assert thread["other_user_id"] == user2.id


def test_delete_message(db_session: Session):
    """Test deleting a message"""
    sender = user_factory(db_session, email="sender5@test.com")
    receiver = user_factory(db_session, email="receiver5@test.com")

    msg_data = MessageCreate(receiver_id=receiver.id, content="Test message")
    message = message_service.send_message(db_session, sender.id, msg_data)
    message_id = message.id

    # Delete message (sender deleting)
    result = message_service.delete_message(db_session, sender.id, message_id)
    assert result == True


def test_delete_message_unauthorized(db_session: Session):
    """Test that unauthorized user cannot delete message"""
    sender = user_factory(db_session, email="sender6@test.com")
    receiver = user_factory(db_session, email="receiver6@test.com")
    other_user = user_factory(db_session, email="other@test.com")

    msg_data = MessageCreate(receiver_id=receiver.id, content="Test message")
    message = message_service.send_message(db_session, sender.id, msg_data)

    # Other user tries to delete (should fail)
    with pytest.raises(Exception) as exc:
        message_service.delete_message(db_session, other_user.id, message.id)

    assert "not found or unauthorized" in str(exc.value)


def test_cannot_send_to_self(db_session: Session):
    """Test that users cannot send messages to themselves"""
    user = user_factory(db_session, email="user@test.com")

    msg_data = MessageCreate(receiver_id=user.id, content="Message to self")

    with pytest.raises(Exception) as exc:
        message_service.send_message(db_session, user.id, msg_data)

    assert "Cannot send message to yourself" in str(exc.value)


def test_cannot_send_to_nonexistent_user(db_session: Session):
    """Test that sending to non-existent user fails"""
    sender = user_factory(db_session, email="sender7@test.com")

    msg_data = MessageCreate(receiver_id=99999, content="Test message")

    with pytest.raises(Exception) as exc:
        message_service.send_message(db_session, sender.id, msg_data)

    assert "Receiver not found" in str(exc.value)
