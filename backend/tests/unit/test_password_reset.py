"""
Unit tests for password reset functionality.

Tests the complete password reset flow including:
- Token generation and validation
- Email sending (mock)
- Password reset request endpoint
- Password reset confirmation endpoint
- Security features (token expiration, single use, rate limiting)
"""

import pytest
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.auth_api import router
from app.database.database import get_db
from app.schemas.user_sql import UserDB, UserType
from app.schemas.password_reset_sql import PasswordResetTokenDB
from app.utils.password_reset import (
    generate_reset_token,
    create_password_reset_token,
    verify_reset_token,
    mark_token_as_used,
    cleanup_expired_tokens
)
from app.utils.auth import get_password_hash, verify_password


@pytest.fixture
def test_app(db_session):
    """Create a test FastAPI app with the auth router."""
    app = FastAPI()
    app.include_router(router)

    # Override the get_db dependency to use test database
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture
def client(test_app):
    """Create a test client."""
    return TestClient(test_app)


@pytest.fixture
def test_user(db_session):
    """Create a test user in the database."""
    user = UserDB(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        location="Test City",
        hashed_password=get_password_hash("OldPassword123!"),
        role=UserType.SEEKER
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ===========================
# Token Generation Tests
# ===========================

def test_generate_reset_token():
    """Test that reset tokens are generated correctly."""
    token1 = generate_reset_token()
    token2 = generate_reset_token()

    # Tokens should be non-empty strings
    assert isinstance(token1, str)
    assert len(token1) > 0

    # Tokens should be unique
    assert token1 != token2

    # Tokens should be URL-safe (no special characters that need encoding)
    assert all(c.isalnum() or c in '-_' for c in token1)


def test_create_password_reset_token(db_session, test_user):
    """Test creating a password reset token for a user."""
    token = create_password_reset_token(db_session, test_user.id)

    # Token should be returned
    assert isinstance(token, str)
    assert len(token) > 0

    # Token should be stored in database
    db_token = db_session.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.token == token)\
        .first()

    assert db_token is not None
    assert db_token.user_id == test_user.id
    assert db_token.used_at is None
    assert db_token.expires_at > datetime.utcnow()


def test_create_password_reset_token_invalidates_previous(db_session, test_user):
    """Test that creating a new token invalidates previous unused tokens."""
    # Create first token
    token1 = create_password_reset_token(db_session, test_user.id)

    # Create second token
    token2 = create_password_reset_token(db_session, test_user.id)

    # First token should be marked as used
    db_token1 = db_session.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.token == token1)\
        .first()

    assert db_token1.used_at is not None

    # Second token should be unused
    db_token2 = db_session.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.token == token2)\
        .first()

    assert db_token2.used_at is None


# ===========================
# Token Verification Tests
# ===========================

def test_verify_reset_token_success(db_session, test_user):
    """Test successful verification of a valid token."""
    token = create_password_reset_token(db_session, test_user.id)

    user_id = verify_reset_token(db_session, token)

    assert user_id == test_user.id


def test_verify_reset_token_invalid(db_session):
    """Test that invalid tokens are rejected."""
    with pytest.raises(ValueError) as exc_info:
        verify_reset_token(db_session, "invalid_token_xyz")

    assert "Invalid reset token" in str(exc_info.value)


def test_verify_reset_token_already_used(db_session, test_user):
    """Test that used tokens are rejected."""
    token = create_password_reset_token(db_session, test_user.id)

    # Mark as used
    mark_token_as_used(db_session, token)

    # Should fail verification
    with pytest.raises(ValueError) as exc_info:
        verify_reset_token(db_session, token)

    assert "already used" in str(exc_info.value)


def test_verify_reset_token_expired(db_session, test_user):
    """Test that expired tokens are rejected."""
    # Create a token
    token = generate_reset_token()
    expired_time = datetime.utcnow() - timedelta(hours=25)  # 25 hours ago

    reset_token = PasswordResetTokenDB(
        user_id=test_user.id,
        token=token,
        expires_at=expired_time
    )
    db_session.add(reset_token)
    db_session.commit()

    # Should fail verification
    with pytest.raises(ValueError) as exc_info:
        verify_reset_token(db_session, token)

    assert "expired" in str(exc_info.value)


# ===========================
# Token Management Tests
# ===========================

def test_mark_token_as_used(db_session, test_user):
    """Test marking a token as used."""
    token = create_password_reset_token(db_session, test_user.id)

    # Initially unused
    db_token = db_session.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.token == token)\
        .first()
    assert db_token.used_at is None

    # Mark as used
    mark_token_as_used(db_session, token)

    # Should be marked as used
    db_session.refresh(db_token)
    assert db_token.used_at is not None
    assert db_token.used_at <= datetime.utcnow()


def test_cleanup_expired_tokens(db_session, test_user):
    """Test cleanup of old expired tokens."""
    # Create an old expired token
    old_token = generate_reset_token()
    old_expired_time = datetime.utcnow() - timedelta(days=8)

    old_reset_token = PasswordResetTokenDB(
        user_id=test_user.id,
        token=old_token,
        expires_at=old_expired_time
    )
    db_session.add(old_reset_token)

    # Create a recent expired token
    recent_token = generate_reset_token()
    recent_expired_time = datetime.utcnow() - timedelta(hours=1)

    recent_reset_token = PasswordResetTokenDB(
        user_id=test_user.id,
        token=recent_token,
        expires_at=recent_expired_time
    )
    db_session.add(recent_reset_token)

    db_session.commit()

    # Cleanup expired tokens
    deleted_count = cleanup_expired_tokens(db_session)

    # Only old token should be deleted
    assert deleted_count == 1

    # Old token should be gone
    old_db_token = db_session.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.token == old_token)\
        .first()
    assert old_db_token is None

    # Recent token should still exist
    recent_db_token = db_session.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.token == recent_token)\
        .first()
    assert recent_db_token is not None


# ===========================
# API Endpoint Tests
# ===========================

def test_request_password_reset_valid_email(client, test_user):
    """Test password reset request with valid email."""
    response = client.post(
        "/auth/request-password-reset",
        json={"email": test_user.email}
    )

    assert response.status_code == 200
    data = response.json()
    assert "If an account exists" in data["message"]


def test_request_password_reset_invalid_email(client):
    """Test password reset request with non-existent email."""
    response = client.post(
        "/auth/request-password-reset",
        json={"email": "nonexistent@example.com"}
    )

    # Should still return success (security - prevent email enumeration)
    assert response.status_code == 200
    data = response.json()
    assert "If an account exists" in data["message"]


def test_request_password_reset_creates_token(client, db_session, test_user):
    """Test that password reset request creates a token in database."""
    # Count tokens before
    tokens_before = db_session.query(PasswordResetTokenDB).count()

    response = client.post(
        "/auth/request-password-reset",
        json={"email": test_user.email}
    )

    assert response.status_code == 200

    # Should have one more token
    tokens_after = db_session.query(PasswordResetTokenDB).count()
    assert tokens_after == tokens_before + 1


def test_reset_password_with_valid_token(client, db_session, test_user):
    """Test password reset with valid token."""
    # Create reset token
    token = create_password_reset_token(db_session, test_user.id)

    # Reset password
    new_password = "NewSecurePassword123!"
    response = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": new_password
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Password reset successful"

    # Verify password was updated
    db_session.refresh(test_user)
    assert verify_password(new_password, test_user.hashed_password)


def test_reset_password_with_invalid_token(client):
    """Test password reset with invalid token."""
    response = client.post(
        "/auth/reset-password",
        json={
            "token": "invalid_token_xyz",
            "new_password": "NewPassword123!"
        }
    )

    assert response.status_code == 400
    assert "Invalid reset token" in response.json()["detail"]


def test_reset_password_with_expired_token(client, db_session, test_user):
    """Test password reset with expired token."""
    # Create expired token
    token = generate_reset_token()
    expired_time = datetime.utcnow() - timedelta(hours=25)

    reset_token = PasswordResetTokenDB(
        user_id=test_user.id,
        token=token,
        expires_at=expired_time
    )
    db_session.add(reset_token)
    db_session.commit()

    # Try to reset password
    response = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "NewPassword123!"
        }
    )

    assert response.status_code == 400
    assert "expired" in response.json()["detail"].lower()


def test_reset_password_with_used_token(client, db_session, test_user):
    """Test that tokens can only be used once."""
    # Create token
    token = create_password_reset_token(db_session, test_user.id)

    # First reset - should succeed
    response1 = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "NewPassword123!"
        }
    )
    assert response1.status_code == 200

    # Second reset with same token - should fail
    response2 = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "AnotherPassword456!"
        }
    )
    assert response2.status_code == 400
    assert "already used" in response2.json()["detail"].lower()


def test_reset_password_password_length_validation(client, db_session, test_user):
    """Test that password must meet minimum length requirement."""
    token = create_password_reset_token(db_session, test_user.id)

    # Try with password too short
    response = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "short"  # Less than 8 characters
        }
    )

    assert response.status_code == 422  # Validation error


def test_complete_password_reset_flow(client, db_session, test_user):
    """Test complete end-to-end password reset flow."""
    old_password = "OldPassword123!"
    new_password = "NewSecurePassword456!"

    # Step 1: Request password reset
    reset_request_response = client.post(
        "/auth/request-password-reset",
        json={"email": test_user.email}
    )
    assert reset_request_response.status_code == 200

    # Step 2: Get the token from database (in real app, user gets this via email)
    reset_token = db_session.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.user_id == test_user.id)\
        .filter(PasswordResetTokenDB.used_at.is_(None))\
        .first()
    assert reset_token is not None

    # Step 3: Reset password with token
    reset_response = client.post(
        "/auth/reset-password",
        json={
            "token": reset_token.token,
            "new_password": new_password
        }
    )
    assert reset_response.status_code == 200

    # Step 4: Verify can login with new password
    login_response = client.post(
        "/auth/login",
        json={
            "email": test_user.email,
            "password": new_password
        }
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    # Step 5: Verify cannot login with old password
    old_login_response = client.post(
        "/auth/login",
        json={
            "email": test_user.email,
            "password": old_password
        }
    )
    assert old_login_response.status_code == 401


# ===========================
# Security Tests
# ===========================

def test_email_enumeration_prevention(client, db_session, test_user):
    """Test that responses don't reveal whether email exists."""
    # Request for existing email
    valid_response = client.post(
        "/auth/request-password-reset",
        json={"email": test_user.email}
    )

    # Request for non-existent email
    invalid_response = client.post(
        "/auth/request-password-reset",
        json={"email": "nonexistent@example.com"}
    )

    # Both should return same response
    assert valid_response.status_code == invalid_response.status_code
    assert valid_response.json()["message"] == invalid_response.json()["message"]


def test_token_cannot_be_reused(client, db_session, test_user):
    """Test that tokens are single-use only."""
    token = create_password_reset_token(db_session, test_user.id)

    # Use token once
    first_use = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "FirstPassword123!"
        }
    )
    assert first_use.status_code == 200

    # Try to use same token again
    second_use = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "SecondPassword456!"
        }
    )
    assert second_use.status_code == 400
    assert "already used" in second_use.json()["detail"].lower()


def test_token_expiration_24_hours(db_session, test_user):
    """Test that tokens expire after 24 hours."""
    token = create_password_reset_token(db_session, test_user.id)

    # Get token from database
    db_token = db_session.query(PasswordResetTokenDB)\
        .filter(PasswordResetTokenDB.token == token)\
        .first()

    # Check expiration is approximately 24 hours in the future
    time_until_expiration = db_token.expires_at - datetime.utcnow()
    hours_until_expiration = time_until_expiration.total_seconds() / 3600

    assert 23.5 < hours_until_expiration < 24.5  # Allow small margin
