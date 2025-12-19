from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.models.auth_pyd import Token, RefreshTokenRequest
from app.models.user_pyd import UserData, UserLogin
from app.schemas.user_sql import UserDB as User
from app.database.database import get_db
from app.services.auth_service import create_user, login_user, get_user, refresh_access_token
from app.middleware.auth_middleware import get_current_user
from app.utils.password_reset import create_password_reset_token, verify_reset_token, mark_token_as_used
from app.utils.email import send_password_reset_email, send_password_reset_confirmation
from app.utils.auth import get_password_hash

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/auth/register", response_model=dict)
@limiter.limit("5/hour")  # 5 registrations per hour per IP
async def register(request: Request, user_data: UserData, db: Session = Depends(get_db)):
    return create_user(user_data, db)

@router.post("/auth/login", response_model=Token)
@limiter.limit("10/minute")  # 10 login attempts per minute per IP
async def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    return login_user(credentials, db)

@router.post("/auth/refresh", response_model=Token)
@limiter.limit("20/minute")  # 20 refresh attempts per minute per IP
async def refresh_token(
    request: Request,
    token_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using a valid refresh token.

    When the access token expires, clients can use their refresh token
    to obtain a new access token without requiring the user to log in again.

    Args:
        token_request: Contains the refresh token
        db: Database session

    Returns:
        Token: New access token with expiration time

    Raises:
        HTTPException 401: If refresh token is invalid or expired
    """
    return refresh_access_token(token_request.refresh_token, db)


@router.get("/auth/me", response_model=UserData)
async def get_me(current_user: User = Depends(get_current_user)):
    return get_user(current_user)


# ===========================
# Password Reset Endpoints
# ===========================

class PasswordResetRequest(BaseModel):
    """Request model for password reset."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Request model for confirming password reset."""
    token: str
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")


@router.post("/auth/request-password-reset")
@limiter.limit("3/hour")  # 3 password reset requests per hour per IP
async def request_password_reset(
    request: Request,
    reset_request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Request a password reset link.

    Sends a password reset email to the user if the email exists in the system.
    Always returns success to prevent email enumeration attacks.

    Security Features:
    - Rate limited to 3 requests/hour per IP
    - Always returns success (prevents account enumeration)
    - Invalidates previous reset tokens
    - Tokens expire after 24 hours

    Args:
        reset_request: Contains the user's email address
        db: Database session

    Returns:
        dict: Success message (same for valid and invalid emails)

    Example:
        >>> POST /auth/request-password-reset
        >>> {"email": "user@example.com"}
        >>> Response: {"message": "If an account exists..."}
    """
    # Look up user
    user = db.query(User).filter(User.email == reset_request.email).first()

    if user:
        # Generate reset token
        reset_token = create_password_reset_token(db, user.id)

        # Send email with reset link
        user_name = f"{user.first_name} {user.last_name}" if user.first_name else None
        send_password_reset_email(user.email, reset_token, user_name)

    # Always return success to prevent email enumeration
    # (Same response whether email exists or not)
    return {
        "message": "If an account exists with that email, a password reset link has been sent."
    }


@router.post("/auth/reset-password")
@limiter.limit("5/hour")  # 5 password reset attempts per hour per IP
async def reset_password(
    request: Request,
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """
    Reset password using a valid reset token.

    Validates the token and updates the user's password.
    Tokens can only be used once and expire after 24 hours.

    Args:
        reset_data: Contains reset token and new password
        db: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException 400: If token is invalid, expired, or already used
        HTTPException 404: If user not found

    Example:
        >>> POST /auth/reset-password
        >>> {
        ...   "token": "abc123...",
        ...   "new_password": "NewSecurePassword123!"
        ... }
        >>> Response: {"message": "Password reset successful"}
    """
    try:
        # Verify token and get user ID
        user_id = verify_reset_token(db, reset_data.token)

        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update password
        user.hashed_password = get_password_hash(reset_data.new_password)

        # Mark token as used (prevents reuse)
        mark_token_as_used(db, reset_data.token)

        # Commit changes
        db.commit()

        # Send confirmation email
        user_name = f"{user.first_name} {user.last_name}" if user.first_name else None
        send_password_reset_confirmation(user.email, user_name)

        return {"message": "Password reset successful"}

    except ValueError as e:
        # Token validation errors (invalid, expired, already used)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )