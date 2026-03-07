from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, case
from app.schemas.message_sql import MessageDB
from app.schemas.user_sql import UserDB
from app.models.message_pyd import MessageCreate, ConversationPreview, MessageResponse
from typing import List
from fastapi import HTTPException
from app.services import notifications_service


def send_message(db: Session, sender_email: str, message_data: MessageCreate) -> MessageDB:
    receiver = db.query(UserDB).filter(UserDB.email == message_data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    if sender_email == message_data.receiver_id:
        raise HTTPException(status_code=400, detail="Cannot send message to yourself")

    sender = db.query(UserDB).filter(UserDB.email == sender_email).first()

    new_message = MessageDB(
        sender_id=sender_email,
        receiver_id=message_data.receiver_id,
        content=message_data.content,
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    if sender:
        sender_name = f"{sender.first_name} {sender.last_name}".strip() or "A user"
        try:
            notifications_service.notify_new_message(
                db=db,
                receiver_email=message_data.receiver_id,
                sender_email=sender_email,
                sender_name=sender_name,
                message_preview=message_data.content,
                message_id=new_message.message_id,
            )
        except Exception as e:
            print(f"Failed to create notification: {e}")

    return new_message


def get_conversations(db: Session, user_email: str) -> List[ConversationPreview]:
    conversations = db.query(
        case(
            (MessageDB.sender_id == user_email, MessageDB.receiver_id),
            else_=MessageDB.sender_id,
        ).label("other_user_email"),
        func.max(MessageDB.created_at).label("last_message_time"),
    ).filter(
        or_(MessageDB.sender_id == user_email, MessageDB.receiver_id == user_email)
    ).group_by("other_user_email").all()

    result = []
    for conv in conversations:
        other_email = conv.other_user_email

        other_user = db.query(UserDB).filter(UserDB.email == other_email).first()
        if not other_user:
            continue

        last_message = db.query(MessageDB).filter(
            or_(
                and_(MessageDB.sender_id == user_email, MessageDB.receiver_id == other_email),
                and_(MessageDB.sender_id == other_email, MessageDB.receiver_id == user_email),
            )
        ).order_by(MessageDB.created_at.desc()).first()

        result.append(ConversationPreview(
            user_id=other_email,
            user_name=f"{other_user.first_name} {other_user.last_name}",
            last_message=last_message.content[:100] if last_message else "",
            last_message_time=conv.last_message_time,
        ))

    result.sort(key=lambda x: x.last_message_time, reverse=True)
    return result


def get_conversation_thread(
    db: Session,
    user_email: str,
    other_email: str,
    skip: int = 0,
    limit: int = 50,
) -> dict:
    other_user = db.query(UserDB).filter(UserDB.email == other_email).first()
    if not other_user:
        raise HTTPException(status_code=404, detail="User not found")

    messages = db.query(MessageDB).filter(
        or_(
            and_(MessageDB.sender_id == user_email, MessageDB.receiver_id == other_email),
            and_(MessageDB.sender_id == other_email, MessageDB.receiver_id == user_email),
        )
    ).order_by(MessageDB.created_at.asc()).offset(skip).limit(limit).all()

    total = db.query(MessageDB).filter(
        or_(
            and_(MessageDB.sender_id == user_email, MessageDB.receiver_id == other_email),
            and_(MessageDB.sender_id == other_email, MessageDB.receiver_id == user_email),
        )
    ).count()

    message_responses = []
    for msg in messages:
        sender = db.query(UserDB).filter(UserDB.email == msg.sender_id).first()
        receiver = db.query(UserDB).filter(UserDB.email == msg.receiver_id).first()

        msg_response = MessageResponse.model_validate(msg)
        msg_response.sender_name = f"{sender.first_name} {sender.last_name}" if sender else "Unknown"
        msg_response.receiver_name = f"{receiver.first_name} {receiver.last_name}" if receiver else "Unknown"
        message_responses.append(msg_response)

    return {
        "other_user_id": other_email,
        "other_user_name": f"{other_user.first_name} {other_user.last_name}",
        "messages": message_responses,
        "total_messages": total,
    }


def delete_message(db: Session, user_email: str, message_id: int) -> bool:
    message = db.query(MessageDB).filter(
        MessageDB.message_id == message_id,
        or_(MessageDB.sender_id == user_email, MessageDB.receiver_id == user_email),
    ).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found or unauthorized")

    db.delete(message)
    db.commit()
    return True
