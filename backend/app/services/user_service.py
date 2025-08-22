from sqlalchemy.orm import Session
from app.schemas.user_sql import UserDB
from app.models.user_pyd import UserRequest


def create_user(db: Session, user: UserRequest):
    # Convert Pydantic model to SQLAlchemy model
    db_user = UserDB(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()

def list_users(db: Session, skip:int=0, limit:int=10):
    return db.query(UserDB).offset(skip).limit(limit).all()
