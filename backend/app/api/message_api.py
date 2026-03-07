from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.middleware.auth_middleware import get_current_user
from app.schemas.user_sql import UserDB
from app.models.message_pyd import MessageCreate, MessageResponse, ConversationPreview
from app.services import message_service
from typing import List
from app.database.database import get_db

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/send", response_model=MessageResponse)
def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    message = message_service.send_message(db, current_user.email, message_data)
    return MessageResponse.model_validate(message)


@router.get("/conversations", response_model=List[ConversationPreview])
def list_conversations(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    return message_service.get_conversations(db, current_user.email)


@router.get("/conversation/{other_user_email}")
def get_conversation(
    other_user_email: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    return message_service.get_conversation_thread(
        db, current_user.email, other_user_email, skip, limit
    )


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    message_service.delete_message(db, current_user.email, message_id)
    return {"success": True, "message": "Message deleted successfully"}
