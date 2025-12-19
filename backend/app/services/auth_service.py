from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.auth_pyd import Token
from app.models.user_pyd import UserData, UserLogin
from app.schemas.user_sql import UserDB as User, UserType
from app.utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.utils.validators import (
    validate_password_strength,
    validate_email_domain,
    validate_user_registration
)


def create_user(user_data: UserData, db: Session):
    # Validate user registration data
    is_valid, validation_errors = validate_user_registration(
        email=user_data.email,
        password=user_data.password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        location=user_data.location
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Validation failed",
                "errors": validation_errors
            }
        )

    # Check if email already exists
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

    # Create both access and refresh tokens
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # in seconds
    }


def refresh_access_token(refresh_token: str, db: Session):
    """
    Generate a new access token using a valid refresh token.

    Args:
        refresh_token: The refresh token
        db: Database session

    Returns:
        dict: New access token and metadata

    Raises:
        HTTPException: If refresh token is invalid or user not found
    """
    try:
        # Verify and decode the refresh token
        token_data = verify_refresh_token(refresh_token)
        email = token_data.get("email")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # Verify user still exists
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        # Create new access token
        access_token = create_access_token(data={"sub": user.email})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )


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