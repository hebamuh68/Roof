from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.services.user_service import list_users, get_user_by_id, create_user, update_user, delete_user
from app.models.user_pyd import UserRequest, UserUpdate

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


@router.post("/users")
def create(user: UserRequest,db: Session = Depends(get_db)):
    return create_user(db,user)

@router.get("/users/{user_id}")
def get(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)


@router.get("/users")
def list(skip:int=0, limit:int=10, db: Session = Depends(get_db)):
    return list_users(db, skip, limit)

@router.put("/users/{user_id}")
def update(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user_update)

@router.delete("/users/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)