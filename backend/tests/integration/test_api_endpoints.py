import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.utils.auth import create_access_token
from tests.conftest import user_factory

client = TestClient(app)


class TestAuthEndpoints:
    """Integration tests for authentication endpoints."""

    def test_register_endpoint_success(self, db_session: Session):
        """Test successful user registration."""
        # Arrange
        user_data = {
            "email": "register@test.com",
            "password": "SecurePass123!",
            "first_name": "Test",
            "last_name": "User",
            "location": "Sydney",
            "role": "SEEKER"
        }

        # Act
        response = client.post("/auth/register", json=user_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_register_endpoint_duplicate_email(self, db_session: Session):
        """Test registration with duplicate email fails."""
        # Arrange
        user = user_factory(db_session, email="duplicate@test.com")
        user_data = {
            "email": "duplicate@test.com",
            "password": "SecurePass123!",
            "first_name": "Test",
            "last_name": "User",
            "location": "Sydney",
            "role": "SEEKER"
        }

        # Act
        response = client.post("/auth/register", json=user_data)

        # Assert
        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower() or "already" in response.json()["detail"].lower()

    def test_login_endpoint_success(self, db_session: Session):
        """Test successful user login."""
        # Arrange
        from app.services.auth_service import create_user
        from app.models.user_pyd import UserData
        user_data = UserData(
            email="login@test.com",
            password="SecurePass123!",
            first_name="Test",
            last_name="User",
            location="Sydney",
            role="SEEKER"
        )
        create_user(user_data, db_session)

        login_data = {
            "email": "login@test.com",
            "password": "SecurePass123!"
        }

        # Act
        response = client.post("/auth/login", json=login_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_endpoint_invalid_credentials(self, db_session: Session):
        """Test login with invalid credentials fails."""
        # Arrange
        login_data = {
            "email": "nonexistent@test.com",
            "password": "WrongPassword123!"
        }

        # Act
        response = client.post("/auth/login", json=login_data)

        # Assert
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower() or "credentials" in response.json()["detail"].lower()

    def test_get_current_user_endpoint(self, db_session: Session):
        """Test getting current user with valid token."""
        # Arrange
        user = user_factory(db_session, email="current@test.com")
        token = create_access_token({"sub": user.email})

        # Act
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "current@test.com"
        assert data["id"] == user.id

    def test_get_current_user_endpoint_no_token(self, db_session: Session):
        """Test getting current user without token fails."""
        # Act
        response = client.get("/auth/me")

        # Assert
        assert response.status_code == 403

    def test_get_current_user_endpoint_invalid_token(self, db_session: Session):
        """Test getting current user with invalid token fails."""
        # Act
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )

        # Assert
        assert response.status_code == 401


class TestApartmentEndpoints:
    """Integration tests for apartment endpoints."""

    def test_get_apartments_list(self, db_session: Session):
        """Test getting list of apartments."""
        # Act
        response = client.get("/apartments?skip=0&limit=10")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_apartment_by_id_not_found(self, db_session: Session):
        """Test getting non-existent apartment returns 404."""
        # Act
        response = client.get("/apartments/99999")

        # Assert
        assert response.status_code == 404

    def test_create_apartment_requires_auth(self, db_session: Session):
        """Test creating apartment without authentication fails."""
        # Act
        response = client.post("/apartments")

        # Assert
        assert response.status_code == 403  # Forbidden - no auth

    def test_get_apartments_with_pagination(self, db_session: Session):
        """Test apartment list pagination."""
        # Act
        response = client.get("/apartments?skip=0&limit=5")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5


class TestUserEndpoints:
    """Integration tests for user endpoints."""

    def test_update_user_requires_auth(self, db_session: Session):
        """Test updating user without authentication fails."""
        # Act
        response = client.put("/users/1", json={"first_name": "New"})

        # Assert
        assert response.status_code == 403

    def test_update_user_with_auth(self, db_session: Session):
        """Test updating user with valid authentication."""
        # Arrange
        user = user_factory(db_session, email="update@test.com")
        token = create_access_token({"sub": user.email})

        update_data = {
            "first_name": "Updated"
        }

        # Act
        response = client.put(
            f"/users/{user.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Updated"

    def test_delete_user_requires_auth(self, db_session: Session):
        """Test deleting user without authentication fails."""
        # Act
        response = client.delete("/users/1")

        # Assert
        assert response.status_code == 403


class TestSearchEndpoints:
    """Integration tests for search endpoints."""

    def test_search_apartments_endpoint(self, db_session: Session):
        """Test search apartments endpoint."""
        # Act
        response = client.get("/search/apartments?query=sydney")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "hits" in data or isinstance(data, dict)

    def test_search_apartments_with_fuzziness(self, db_session: Session):
        """Test search with fuzziness parameter."""
        # Act
        response = client.get("/search/apartments?query=sydney&fuzziness=1")

        # Assert
        assert response.status_code == 200

    def test_autocomplete_endpoint(self, db_session: Session):
        """Test autocomplete endpoint."""
        # Act
        response = client.get("/autocomplete?query=syd")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_filter_apartments_endpoint(self, db_session: Session):
        """Test filter apartments endpoint."""
        # Arrange
        filter_data = {
            "location": "Sydney",
            "rent_per_week": 500
        }

        # Act
        response = client.post("/filter/apartments", json=filter_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "hits" in data or isinstance(data, dict)


class TestMessageEndpoints:
    """Integration tests for message endpoints."""

    def test_send_message_requires_auth(self, db_session: Session):
        """Test sending message without authentication fails."""
        # Arrange
        message_data = {
            "receiver_id": 1,
            "content": "Test message"
        }

        # Act
        response = client.post("/messages/send", json=message_data)

        # Assert
        assert response.status_code == 403

    def test_get_conversations_requires_auth(self, db_session: Session):
        """Test getting conversations without authentication fails."""
        # Act
        response = client.get("/messages/conversations")

        # Assert
        assert response.status_code == 403


class TestNotificationEndpoints:
    """Integration tests for notification endpoints."""

    def test_get_notifications_requires_auth(self, db_session: Session):
        """Test getting notifications without authentication fails."""
        # Act
        response = client.get("/notifications/")

        # Assert
        assert response.status_code == 403

    def test_get_unread_count_requires_auth(self, db_session: Session):
        """Test getting unread count without authentication fails."""
        # Act
        response = client.get("/notifications/unread-count")

        # Assert
        assert response.status_code == 403


class TestAdminEndpoints:
    """Integration tests for admin endpoints."""

    def test_admin_users_requires_auth(self, db_session: Session):
        """Test admin endpoints require authentication."""
        # Act
        response = client.get("/admin/users")

        # Assert
        assert response.status_code == 403

    def test_admin_stats_requires_auth(self, db_session: Session):
        """Test admin stats endpoint requires authentication."""
        # Act
        response = client.get("/admin/stats")

        # Assert
        assert response.status_code == 403

