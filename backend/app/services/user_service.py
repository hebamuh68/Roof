from sqlalchemy.orm import Session
from app.schemas.user_sql import UserDB
from app.models.user_pyd import UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def update_user(db: Session, email: str, user_update: UserUpdate):
    db_user = db.query(UserDB).filter(UserDB.email == email).first()
    if not db_user:
        return None

    user_clean = user_update.model_dump(exclude_unset=True)

    if "password" in user_clean:
        user_clean["hashed_password"] = pwd_context.hash(user_clean.pop("password"))

    for field, value in user_clean.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, email: str):
    db_user = db.query(UserDB).filter(UserDB.email == email).first()
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return {"message": f"User {email} deleted successfully"}


def list_all_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return [
        {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "gender": user.gender,
            "dob": user.dob,
            "job_title": user.job_title,
            "is_admin": user.is_admin,
        }
        for user in users
    ]


def get_user_by_email(db: Session, email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()
