from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.auth_pyd import UserCreate, UserLogin, Token
from app.schemas.user_sql import UserDB as User, UserType
from app.utils.auth import get_password_hash, verify_password, create_access_token


def create_user(user_data: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Convert role string to enum
    role_enum = UserType.SEEKER if user_data.role == "seeker" else UserType.RENTER

    # Create new user
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        location=user_data.location,
        flatmate_pref=user_data.flatmate_pref or [],
        keywords=user_data.keywords or [],
        hashed_password=hashed_password,
        role=role_enum
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}


def login_user(credentials: UserLogin, db: Session):
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    # Check if user exists and password is correct
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def get_user(current_user: User):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "location": current_user.location,
        "flatmate_pref": current_user.flatmate_pref,
        "keywords": current_user.keywords,
        "role": current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role),
        "created_at": getattr(current_user, 'created_at', None)
    }