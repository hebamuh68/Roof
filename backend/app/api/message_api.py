from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.schemas.user_sql import UserDB
from app.models.message_pyd import (
    MessageCreate,
    MessageResponse,
    ConversationPreview,
)
from app.services import message_service
from typing import List


router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/send", response_model=MessageResponse)
def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Send a new message to another user.

    - **receiver_id**: ID of the user to send message to
    - **content**: Message text content (1-5000 characters)
    """
    message = message_service.send_message(db, current_user.id, message_data)
    return MessageResponse.model_validate(message)


@router.get("/conversations", response_model=List[ConversationPreview])
def list_conversations(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Get all conversations for the current user.

    Returns a list of conversations with:
    - Other user's info
    - Last message preview
    - Last message timestamp
    """
    return message_service.get_conversations(db, current_user.id)


@router.get("/conversation/{other_user_id}")
def get_conversation(
    other_user_id: int,
    skip: int = Query(0, ge=0, description="Number of messages to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum messages to return"),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Get full conversation thread with another user.

    Returns all messages between current user and specified user,
    ordered chronologically (oldest first).

    Supports pagination with skip/limit.
    """
    return message_service.get_conversation_thread(
        db,
        current_user.id,
        other_user_id,
        skip,
        limit
    )


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Delete a message.

    User must be either sender or receiver of the message.
    """
    message_service.delete_message(db, current_user.id, message_id)

    return {
        "success": True,
        "message": "Message deleted successfully"
    }

