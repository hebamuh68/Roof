"""
Password Reset Utilities.

Provides functions for generating, validating, and managing
password reset tokens.
"""

import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.schemas.password_reset_sql import PasswordResetTokenDB

# Token expires after 24 hours
PASSWORD_RESET_TOKEN_EXPIRE_HOURS = 24


def generate_reset_token() -> str:
    """
    Generate a secure random token for password reset.

    Returns:
        str: A 32-byte URL-safe random token

    Example:
        >>> token = generate_reset_token()
        >>> len(token) >= 40  # URL-safe tokens are longer than raw bytes
        True
    """
    return secrets.token_urlsafe(32)


def create_password_reset_token(db: Session, user_id: int) -> str:
    """
    Create a password reset token for a user.

    This function:
    1. Invalidates any existing unused tokens for the user
    2. Generates a new secure random token
    3. Saves it to the database with 24-hour expiration

    Args:
        db: Database session
        user_id: ID of user requesting reset

    Returns:
        str: The reset token to send to user

    Example:
        >>> token = create_password_reset_token(db, user_id=5)
        >>> # Send token via email to user
    """
    # Invalidate any existing tokens for this user that haven't been used
    db.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.user_id == user_id)\
        .filter(PasswordResetTokenDB.used_at.is_(None))\
        .update({"used_at": datetime.utcnow()})

    # Generate new token
    token = generate_reset_token()
    expires_at = datetime.utcnow() + timedelta(hours=PASSWORD_RESET_TOKEN_EXPIRE_HOURS)

    # Save to database
    reset_token = PasswordResetTokenDB(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(reset_token)
    db.commit()

    return token


def verify_reset_token(db: Session, token: str) -> int:
    """
    Verify a password reset token and return the user ID.

    Args:
        db: Database session
        token: Reset token to verify

    Returns:
        int: User ID if token is valid

    Raises:
        ValueError: If token is invalid, expired, or already used

    Example:
        >>> try:
        ...     user_id = verify_reset_token(db, token)
        ...     # Reset password for user_id
        ... except ValueError as e:
        ...     print(f"Invalid token: {e}")
    """
    reset_token = db.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.token == token)\
        .first()

    if not reset_token:
        raise ValueError("Invalid reset token")

    if reset_token.used_at:
        raise ValueError("Reset token already used")

    if datetime.utcnow() > reset_token.expires_at:
        raise ValueError("Reset token expired")

    return reset_token.user_id


def mark_token_as_used(db: Session, token: str) -> None:
    """
    Mark a reset token as used.

    This prevents the token from being reused for security.

    Args:
        db: Database session
        token: Token to mark as used

    Example:
        >>> mark_token_as_used(db, token)
        >>> # Token can no longer be used
    """
    db.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.token == token)\
        .update({"used_at": datetime.utcnow()})
    db.commit()


def cleanup_expired_tokens(db: Session) -> int:
    """
    Clean up expired password reset tokens from database.

    This is a maintenance function that should be run periodically
    (e.g., via cron job or scheduled task) to remove old tokens.

    Args:
        db: Database session

    Returns:
        int: Number of tokens deleted

    Example:
        >>> deleted = cleanup_expired_tokens(db)
        >>> print(f"Cleaned up {deleted} expired tokens")
    """
    # Delete tokens that expired more than 7 days ago
    cutoff_date = datetime.utcnow() - timedelta(days=7)

    result = db.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.expires_at < cutoff_date)\
        .delete()

    db.commit()
    return result
