from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from app.schemas.message_sql import MessageDB
from app.schemas.user_sql import UserDB
from app.models.message_pyd import MessageCreate, ConversationPreview, MessageResponse
from typing import List
from fastapi import HTTPException


def send_message(db: Session, sender_id: int, message_data: MessageCreate) -> MessageDB:
    """
    Send a new message from sender to receiver.

    Args:
        db: Database session
        sender_id: ID of the message sender (current user)
        message_data: Message content and recipient info

    Returns:
        Created message object
    """
    # Verify receiver exists
    receiver = db.query(UserDB).filter(UserDB.id == message_data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    # Prevent sending message to self
    if sender_id == message_data.receiver_id:
        raise HTTPException(status_code=400, detail="Cannot send message to yourself")

    # Create message
    new_message = MessageDB(
        sender_id=sender_id,
        receiver_id=message_data.receiver_id,
        content=message_data.content
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


def get_conversations(db: Session, user_id: int) -> List[ConversationPreview]:
    """
    Get all conversations for a user with preview of last message.

    Args:
        db: Database session
        user_id: Current user ID

    Returns:
        List of conversation previews
    """
    # Get all users the current user has exchanged messages with
    conversations = db.query(
        # Determine the other user in the conversation
        func.CASE(
            (MessageDB.sender_id == user_id, MessageDB.receiver_id),
            else_=MessageDB.sender_id
        ).label('other_user_id'),
        func.max(MessageDB.created_at).label('last_message_time')
    ).filter(
        or_(MessageDB.sender_id == user_id, MessageDB.receiver_id == user_id)
    ).group_by('other_user_id').all()

    result = []
    for conv in conversations:
        other_user_id = conv.other_user_id

        # Get other user's name
        other_user = db.query(UserDB).filter(UserDB.id == other_user_id).first()
        if not other_user:
            continue

        # Get last message in conversation
        last_message = db.query(MessageDB).filter(
            or_(
                and_(MessageDB.sender_id == user_id, MessageDB.receiver_id == other_user_id),
                and_(MessageDB.sender_id == other_user_id, MessageDB.receiver_id == user_id)
            )
        ).order_by(MessageDB.created_at.desc()).first()

        result.append(ConversationPreview(
            user_id=other_user_id,
            user_name=f"{other_user.first_name} {other_user.last_name}",
            last_message=last_message.content[:100] if last_message else "",
            last_message_time=conv.last_message_time
        ))

    # Sort by most recent first
    result.sort(key=lambda x: x.last_message_time, reverse=True)

    return result


def get_conversation_thread(
    db: Session,
    user_id: int,
    other_user_id: int,
    skip: int = 0,
    limit: int = 50
) -> dict:
    """
    Get all messages in a conversation between two users.

    Args:
        db: Database session
        user_id: Current user ID
        other_user_id: ID of the other user in the conversation
        skip: Number of messages to skip (pagination)
        limit: Maximum messages to return

    Returns:
        Dictionary with messages and metadata
    """
    # Verify other user exists
    other_user = db.query(UserDB).filter(UserDB.id == other_user_id).first()
    if not other_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all messages between the two users
    messages = db.query(MessageDB).filter(
        or_(
            and_(MessageDB.sender_id == user_id, MessageDB.receiver_id == other_user_id),
            and_(MessageDB.sender_id == other_user_id, MessageDB.receiver_id == user_id)
        )
    ).order_by(MessageDB.created_at.asc()).offset(skip).limit(limit).all()

    # Get total count
    total = db.query(MessageDB).filter(
        or_(
            and_(MessageDB.sender_id == user_id, MessageDB.receiver_id == other_user_id),
            and_(MessageDB.sender_id == other_user_id, MessageDB.receiver_id == user_id)
        )
    ).count()

    # Convert to response models with user names
    message_responses = []
    for msg in messages:
        sender = db.query(UserDB).filter(UserDB.id == msg.sender_id).first()
        receiver = db.query(UserDB).filter(UserDB.id == msg.receiver_id).first()

        msg_response = MessageResponse.model_validate(msg)
        msg_response.sender_name = f"{sender.first_name} {sender.last_name}" if sender else "Unknown"
        msg_response.receiver_name = f"{receiver.first_name} {receiver.last_name}" if receiver else "Unknown"
        message_responses.append(msg_response)

    return {
        "other_user_id": other_user_id,
        "other_user_name": f"{other_user.first_name} {other_user.last_name}",
        "messages": message_responses,
        "total_messages": total
    }


def delete_message(db: Session, user_id: int, message_id: int) -> bool:
    """
    Delete a message (only if user is sender or receiver).

    Args:
        db: Database session
        user_id: Current user ID
        message_id: ID of message to delete

    Returns:
        True if deleted, False if not found or unauthorized
    """
    message = db.query(MessageDB).filter(
        MessageDB.id == message_id,
        or_(MessageDB.sender_id == user_id, MessageDB.receiver_id == user_id)
    ).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found or unauthorized")

    db.delete(message)
    db.commit()

    return True

