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
