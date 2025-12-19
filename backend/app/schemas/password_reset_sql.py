"""
Password Reset Token SQLAlchemy Model.

This model stores password reset tokens for secure password recovery.
Tokens expire after 24 hours and can only be used once.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.database import Base
from datetime import datetime


class PasswordResetTokenDB(Base):
    """
    Password reset token database model.

    Attributes:
        id: Primary key
        user_id: Foreign key to users table
        token: Unique reset token (32-byte URL-safe string)
        created_at: When the token was created
        expires_at: When the token expires (24 hours after creation)
        used_at: When the token was used (NULL if unused)
    """
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)
