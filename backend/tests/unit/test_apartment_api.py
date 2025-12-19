"""
API-level tests for apartment endpoints.

Tests ownership validation and authorization for protected apartment operations.
"""

import pytest
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.apartment_api import router
from app.api.apartment_api import get_db as apartment_get_db
from app.middleware.auth_middleware import get_db as auth_get_db
from app.schemas.user_sql import UserDB
from app.schemas.apartment_sql import ApartmentDB, ApartmentStatus
from app.utils.auth import create_access_token


@pytest.fixture
def test_app(db_session):
    """Create a test FastAPI app with the apartment router."""
    app = FastAPI()
    app.include_router(router)

    # Override the get_db dependency to use test database
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Override both get_db functions (one from apartment_api, one from auth_middleware)
    app.dependency_overrides[apartment_get_db] = override_get_db
    app.dependency_overrides[auth_get_db] = override_get_db
    return app


@pytest.fixture
def client(test_app):
    """Create a test client."""
    return TestClient(test_app)


def create_test_user(db: Session, email: str, first_name: str = "Test") -> UserDB:
    """Helper to create a test user."""
    user = UserDB(
        first_name=first_name,
        last_name="User",
        email=email,
        location="Test City",
        role=UserDB.__table__.c.role.type.python_type.RENTER,
        hashed_password="hashedpass123"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_apartment(db: Session, renter_id: int, title: str = "Test Apartment") -> ApartmentDB:
    """Helper to create a test apartment."""
    apartment = ApartmentDB(
        title=title,
        description="Test description",
        location="Test City",
        apartment_type="Studio",
        rent_per_week=500,
        start_date=datetime.now(timezone.utc),
        place_accept="Both",
        furnishing_type="Furnished",
        is_pathroom_solo=True,
        parking_type="None",
        is_active=True,
        status=ApartmentStatus.PUBLISHED,
        renter_id=renter_id,
        images=["test1.jpg", "test2.jpg", "test3.jpg", "test4.jpg"]
    )
    db.add(apartment)
    db.commit()
    db.refresh(apartment)
    return apartment


def test_update_apartment_ownership_validation(db_session, client):
    """Test that users cannot update apartments they don't own."""
    # Create two users
    user1 = create_test_user(db_session, "user1@test.com", "User1")
    user2 = create_test_user(db_session, "user2@test.com", "User2")

    # User1 creates an apartment
    apartment = create_test_apartment(db_session, user1.id, "User1's Apartment")

    # User2 tries to update user1's apartment
    user2_token = create_access_token(data={"sub": user2.email})
    headers = {"Authorization": f"Bearer {user2_token}"}

    update_data = {
        "title": "Hacked Title",
        "rent_per_week": 99999
    }

    response = client.put(
        f"/apartments/{apartment.id}",
        json=update_data,
        headers=headers
    )

    # Assert: Should receive 403 Forbidden
    assert response.status_code == 403
    assert "permission" in response.json()["detail"].lower()

    # Verify apartment was not modified
    db_session.refresh(apartment)
    assert apartment.title == "User1's Apartment"
    assert apartment.rent_per_week == 500


def test_feature_apartment_ownership_validation(db_session, client):
    """Test that users cannot feature apartments they don't own."""
    # Create two users
    user1 = create_test_user(db_session, "owner@test.com", "Owner")
    user2 = create_test_user(db_session, "hacker@test.com", "Hacker")

    # User1 creates an apartment
    apartment = create_test_apartment(db_session, user1.id, "Owner's Apartment")

    # User2 tries to feature user1's apartment
    user2_token = create_access_token(data={"sub": user2.email})
    headers = {"Authorization": f"Bearer {user2_token}"}

    feature_data = {
        "duration_days": 30,
        "priority": 10
    }

    response = client.post(
        f"/{apartment.id}/feature",
        json=feature_data,
        headers=headers
    )

    # Assert: Should receive 403 Forbidden
    assert response.status_code == 403
    assert "permission" in response.json()["detail"].lower()

    # Verify apartment was not featured
    db_session.refresh(apartment)
    assert apartment.is_featured == False
    assert apartment.featured_priority == 0


def test_update_apartment_ownership_validation_owner_succeeds(db_session, client):
    """Test that the actual owner CAN update their apartment."""
    # Create a user and their apartment
    user = create_test_user(db_session, "realowner@test.com", "RealOwner")
    apartment = create_test_apartment(db_session, user.id, "My Apartment")

    # Owner updates their own apartment
    user_token = create_access_token(data={"sub": user.email})
    headers = {"Authorization": f"Bearer {user_token}"}

    update_data = {
        "title": "My Updated Apartment",
        "rent_per_week": 750
    }

    response = client.put(
        f"/apartments/{apartment.id}",
        json=update_data,
        headers=headers
    )

    # Assert: Should succeed
    assert response.status_code == 200
    assert response.json()["title"] == "My Updated Apartment"
    assert response.json()["rent_per_week"] == 750


def test_feature_apartment_ownership_validation_owner_succeeds(db_session, client):
    """Test that the actual owner CAN feature their apartment."""
    # Create a user and their apartment
    user = create_test_user(db_session, "apartmentowner@test.com", "AptOwner")
    apartment = create_test_apartment(db_session, user.id, "My Premium Apartment")

    # Owner features their own apartment
    user_token = create_access_token(data={"sub": user.email})
    headers = {"Authorization": f"Bearer {user_token}"}

    feature_data = {
        "duration_days": 30,
        "priority": 8
    }

    response = client.post(
        f"/{apartment.id}/feature",
        json=feature_data,
        headers=headers
    )

    # Assert: Should succeed
    assert response.status_code == 200
    assert response.json()["is_featured"] == True
    assert response.json()["featured_priority"] == 8
