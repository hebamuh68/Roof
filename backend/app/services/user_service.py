from sqlalchemy.orm import Session
from app.schemas.user_sql import UserDB, UserType
from app.schemas.apartment_sql import ApartmentDB  # Import to resolve relationship
from app.models.user_pyd import UserRequest
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserRequest):
    db_user = UserDB(
        **user.model_dump(exclude={"password", "role"}),
        role=UserType(user.role.lower()) if user.role else UserType.SEEKER,
        hashed_password=pwd_context.hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()

def list_users(db: Session, skip:int=0, limit:int=10):
    return db.query(UserDB).offset(skip).limit(limit).all()
