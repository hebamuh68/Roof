from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.user_service import update_user
from app.models.user_pyd import UserUpdate
from app.schemas.user_sql import UserDB
from app.middleware.auth_middleware import get_current_user

router = APIRouter()


@router.put("/users/me")
def update_current_user(
    user_update: UserUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = update_user(db, current_user.email, user_update)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}
