from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.services.user_service import update_user, block_user
from app.models.user_pyd import UserUpdate

router = APIRouter()

# You need to create a new session for each request
# Sessions should be short-lived and closed after use
# DO THIS
def get_db():
    db = SessionLocal()  # New session for each request
    try:
        yield db
    finally:
        db.close()  # Always close the session


@router.put("/users/{user_id}")
def updateUser(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user_update)

@router.delete("/users/{user_id}")
def blockUser(user_id: int, db: Session = Depends(get_db)):
    return block_user(db, user_id)


    