from sqlalchemy.orm import Session
from app.schemas.user_sql import UserDB, UserType
from app.schemas.apartment_sql import ApartmentDB  # Import to resolve relationship
from app.models.user_pyd import UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    # Get the user from database
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        return None
    
    # Update fields
    user_clean = user_update.model_dump(exclude_unset=True)

    if "password" in user_clean: 
        user_clean["hashed_password"] = pwd_context.hash(user_clean.pop("password"))

    if "role" in user_clean:
        user_clean["role"] = UserType(user_clean["role"].upper())

    # Update query
    for field, value in user_clean.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def block_user(db: Session, user_id: int):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        return None
    
    # Block the user
    db.delete(db_user)
    db.commit()
    return {"message": "User blocked successfully"}
