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


def list_all_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users with pagination."""
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "location": user.location,
            "role": user.role.value if hasattr(user.role, 'value') else str(user.role),
            "created_at": user.created_at,
            "flatmate_pref": user.flatmate_pref,
            "keywords": user.keywords
        }
        for user in users
    ]


def get_user_by_id(db: Session, user_id: int):
    """Get a user by their ID."""
    return db.query(UserDB).filter(UserDB.id == user_id).first()


def delete_user(db: Session, user_id: int):
    """Delete a user by their ID."""
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}
