"""
Unit tests for refresh token functionality.

Tests the complete refresh token flow including:
- Token generation and validation
- Token refresh endpoint
- Error handling for invalid/expired tokens
- Security validation (access tokens cannot be used for refresh)
"""

import pytest
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from jose import jwt

from app.api.auth_api import router
from app.database.database import get_db
from app.schemas.user_sql import UserDB, UserType
from app.utils.auth import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    get_password_hash,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)
from app.services.auth_service import login_user, refresh_access_token


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
        hashed_password=get_password_hash("password123"),
        role=UserType.SEEKER
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ===========================
# Token Creation Tests
# ===========================

def test_create_refresh_token_structure():
    """Test that refresh tokens have correct structure."""
    data = {"sub": "test@example.com"}
    refresh_token = create_refresh_token(data)

    # Decode without verification to inspect structure
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "refresh"
    assert "exp" in payload

    # Verify expiration is approximately REFRESH_TOKEN_EXPIRE_DAYS in the future
    exp_time = datetime.fromtimestamp(payload["exp"])
    expected_exp = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    assert abs((exp_time - expected_exp).total_seconds()) < 5  # Within 5 seconds


def test_access_token_does_not_have_type_field():
    """Test that access tokens don't have the 'type' field."""
    data = {"sub": "test@example.com"}
    access_token = create_access_token(data)

    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

    assert "type" not in payload
    assert payload["sub"] == "test@example.com"


# ===========================
# Token Verification Tests
# ===========================

def test_verify_refresh_token_success():
    """Test successful verification of a valid refresh token."""
    data = {"sub": "test@example.com"}
    refresh_token = create_refresh_token(data)

    result = verify_refresh_token(refresh_token)

    assert result["email"] == "test@example.com"


def test_verify_refresh_token_rejects_access_token():
    """Test that access tokens are rejected by refresh token verification."""
    data = {"sub": "test@example.com"}
    access_token = create_access_token(data)

    with pytest.raises(Exception) as exc_info:
        verify_refresh_token(access_token)

    assert "Invalid token type" in str(exc_info.value) or "Invalid refresh token" in str(exc_info.value)


def test_verify_refresh_token_rejects_invalid_token():
    """Test that invalid tokens are rejected."""
    invalid_token = "invalid.token.here"

    with pytest.raises(Exception):
        verify_refresh_token(invalid_token)


def test_verify_refresh_token_rejects_expired_token():
    """Test that expired refresh tokens are rejected."""
    # Create a token that expired 1 day ago
    data = {"sub": "test@example.com"}
    to_encode = data.copy()
    expire = datetime.utcnow() - timedelta(days=1)  # Expired yesterday
    to_encode.update({"exp": expire, "type": "refresh"})
    expired_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(Exception):
        verify_refresh_token(expired_token)


# ===========================
# Login Service Tests
# ===========================

def test_login_returns_both_tokens(db_session, test_user):
    """Test that login returns both access and refresh tokens."""
    from app.models.user_pyd import UserLogin

    credentials = UserLogin(
        email="test@example.com",
        password="password123"
    )

    result = login_user(credentials, db_session)

    assert "access_token" in result
    assert "refresh_token" in result
    assert "token_type" in result
    assert "expires_in" in result
    assert result["token_type"] == "bearer"
    assert result["expires_in"] == ACCESS_TOKEN_EXPIRE_MINUTES * 60


def test_login_tokens_are_different(db_session, test_user):
    """Test that access and refresh tokens are different."""
    from app.models.user_pyd import UserLogin

    credentials = UserLogin(
        email="test@example.com",
        password="password123"
    )

    result = login_user(credentials, db_session)

    assert result["access_token"] != result["refresh_token"]


# ===========================
# Refresh Token Service Tests
# ===========================

def test_refresh_access_token_success(db_session, test_user):
    """Test successful refresh of access token."""
    # Create a valid refresh token
    refresh_token = create_refresh_token(data={"sub": test_user.email})

    # Refresh the access token
    result = refresh_access_token(refresh_token, db_session)

    assert "access_token" in result
    assert "token_type" in result
    assert "expires_in" in result
    assert result["token_type"] == "bearer"
    assert result["expires_in"] == ACCESS_TOKEN_EXPIRE_MINUTES * 60


def test_refresh_access_token_with_invalid_token(db_session):
    """Test refresh with invalid token."""
    invalid_token = "invalid.token.here"

    with pytest.raises(HTTPException) as exc_info:
        refresh_access_token(invalid_token, db_session)

    assert exc_info.value.status_code == 401
    assert "Invalid or expired refresh token" in exc_info.value.detail


def test_refresh_access_token_with_access_token(db_session, test_user):
    """Test that access tokens cannot be used to refresh."""
    # Create an access token (not refresh)
    access_token = create_access_token(data={"sub": test_user.email})

    with pytest.raises(HTTPException) as exc_info:
        refresh_access_token(access_token, db_session)

    assert exc_info.value.status_code == 401


def test_refresh_access_token_for_nonexistent_user(db_session):
    """Test refresh for a user that doesn't exist."""
    # Create refresh token for non-existent user
    refresh_token = create_refresh_token(data={"sub": "nonexistent@example.com"})

    with pytest.raises(HTTPException) as exc_info:
        refresh_access_token(refresh_token, db_session)

    assert exc_info.value.status_code == 401
    assert "User not found" in exc_info.value.detail or "Invalid" in exc_info.value.detail


# ===========================
# API Endpoint Tests
# ===========================

def test_login_endpoint_returns_tokens(client, test_user):
    """Test /auth/login endpoint returns both tokens."""
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data
    assert "expires_in" in data
    assert data["token_type"] == "bearer"


def test_refresh_endpoint_success(client, test_user):
    """Test /auth/refresh endpoint with valid refresh token."""
    # First, login to get a refresh token
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]

    # Use refresh token to get new access token
    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )

    assert refresh_response.status_code == 200
    data = refresh_response.json()

    assert "access_token" in data
    assert "token_type" in data
    assert "expires_in" in data
    assert data["token_type"] == "bearer"


def test_refresh_endpoint_with_invalid_token(client):
    """Test /auth/refresh with invalid token returns 401."""
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid.token.here"}
    )

    assert response.status_code == 401
    assert "Invalid or expired refresh token" in response.json()["detail"]


def test_refresh_endpoint_with_access_token(client, test_user):
    """Test that /auth/refresh rejects access tokens."""
    # Login to get tokens
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    access_token = login_response.json()["access_token"]

    # Try to use access token for refresh (should fail)
    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": access_token}
    )

    assert refresh_response.status_code == 401


def test_new_access_token_works_for_protected_endpoint(client, test_user):
    """Test that refreshed access token works for protected endpoints."""
    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    refresh_token = login_response.json()["refresh_token"]

    # Refresh to get new access token
    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    new_access_token = refresh_response.json()["access_token"]

    # Use new access token to access protected endpoint
    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {new_access_token}"}
    )

    assert me_response.status_code == 200
    user_data = me_response.json()
    assert user_data["email"] == "test@example.com"


def test_multiple_refresh_operations(client, test_user):
    """Test that refresh token can be used multiple times."""
    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    refresh_token = login_response.json()["refresh_token"]

    # Refresh multiple times
    for i in range(3):
        refresh_response = client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token}
        )

        assert refresh_response.status_code == 200
        data = refresh_response.json()
        assert "access_token" in data

        # Verify each new access token works
        me_response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {data['access_token']}"}
        )
        assert me_response.status_code == 200


# ===========================
# Security Tests
# ===========================

def test_refresh_token_has_longer_expiration_than_access_token():
    """Test that refresh tokens expire later than access tokens."""
    data = {"sub": "test@example.com"}

    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)

    access_payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    refresh_payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

    access_exp = datetime.fromtimestamp(access_payload["exp"])
    refresh_exp = datetime.fromtimestamp(refresh_payload["exp"])

    # Refresh token should expire MUCH later than access token
    assert refresh_exp > access_exp
    # Should be at least 6 days difference (refresh is 7 days, access is 30 min)
    assert (refresh_exp - access_exp).days >= 6


def test_refresh_token_contains_type_marker():
    """Test that refresh tokens are marked with type field for security."""
    refresh_token = create_refresh_token({"sub": "test@example.com"})
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

    assert "type" in payload
    assert payload["type"] == "refresh"
