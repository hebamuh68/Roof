import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.middleware.auth_middleware import get_current_user
from app.schemas.user_sql import UserDB, UserType
from tests.conftest import user_factory


class TestAuthMiddleware:
    """Test suite for authentication middleware."""

    def test_get_current_user_success(self, db_session: Session):
        """Test successful user authentication."""
        # Arrange
        user = user_factory(
            db_session,
            email="auth@test.com",
            first_name="Test",
            last_name="User"
        )

        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "valid_token"

        with patch('app.middleware.auth_middleware.verify_token') as mock_verify:
            mock_verify.return_value = {"email": "auth@test.com"}

            # Act
            result = get_current_user(mock_credentials, db_session)

            # Assert
            assert result is not None
            assert result.id == user.id
            assert result.email == "auth@test.com"
            mock_verify.assert_called_once_with("valid_token")

    def test_get_current_user_invalid_token(self, db_session: Session):
        """Test authentication with invalid JWT token."""
        # Arrange
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "invalid_token"

        with patch('app.middleware.auth_middleware.verify_token') as mock_verify:
            mock_verify.side_effect = JWTError("Invalid token")

            # Act & Assert
            with pytest.raises(HTTPException) as exc:
                get_current_user(mock_credentials, db_session)
            assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Could not validate credentials" in exc.value.detail
            assert "WWW-Authenticate" in exc.value.headers

    def test_get_current_user_missing_token(self, db_session: Session):
        """Test authentication when token is missing."""
        # Arrange
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = None

        with patch('app.middleware.auth_middleware.verify_token') as mock_verify:
            mock_verify.side_effect = JWTError("Missing token")

            # Act & Assert
            with pytest.raises(HTTPException) as exc:
                get_current_user(mock_credentials, db_session)
            assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_not_found(self, db_session: Session):
        """Test authentication when user doesn't exist in database."""
        # Arrange
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "valid_token"

        with patch('app.middleware.auth_middleware.verify_token') as mock_verify:
            mock_verify.return_value = {"email": "nonexistent@test.com"}

            # Act & Assert
            with pytest.raises(HTTPException) as exc:
                get_current_user(mock_credentials, db_session)
            assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Could not validate credentials" in exc.value.detail

    def test_get_current_user_expired_token(self, db_session: Session):
        """Test authentication with expired token."""
        # Arrange
        user = user_factory(db_session, email="expired@test.com")
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "expired_token"

        with patch('app.middleware.auth_middleware.verify_token') as mock_verify:
            from jose.exceptions import ExpiredSignatureError
            mock_verify.side_effect = ExpiredSignatureError("Token expired")

            # Act & Assert
            with pytest.raises(HTTPException) as exc:
                get_current_user(mock_credentials, db_session)
            assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_different_user_types(self, db_session: Session):
        """Test authentication works for different user types."""
        # Arrange - Test SEEKER
        seeker = user_factory(
            db_session,
            email="seeker@test.com",
            role="SEEKER"
        )

        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "token"

        with patch('app.middleware.auth_middleware.verify_token') as mock_verify:
            mock_verify.return_value = {"email": "seeker@test.com"}

            # Act
            result = get_current_user(mock_credentials, db_session)

            # Assert
            assert result.role == UserType.SEEKER

        # Arrange - Test RENTER
        renter = user_factory(
            db_session,
            email="renter@test.com",
            role="RENTER"
        )

        with patch('app.middleware.auth_middleware.verify_token') as mock_verify:
            mock_verify.return_value = {"email": "renter@test.com"}

            # Act
            result = get_current_user(mock_credentials, db_session)

            # Assert
            assert result.role == UserType.RENTER

    def test_get_current_user_token_without_email(self, db_session: Session):
        """Test authentication when token doesn't contain email."""
        # Arrange
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "token"

        with patch('app.middleware.auth_middleware.verify_token') as mock_verify:
            mock_verify.return_value = {"user_id": 123}  # Missing email

            # Act & Assert
            with pytest.raises(KeyError):
                get_current_user(mock_credentials, db_session)

    def test_get_current_user_database_error(self, db_session: Session):
        """Test authentication handles database errors gracefully."""
        # Arrange
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "token"

        with patch('app.middleware.auth_middleware.verify_token') as mock_verify:
            mock_verify.return_value = {"email": "test@test.com"}

            # Mock database query to raise exception
            with patch.object(db_session, 'query') as mock_query:
                mock_query.side_effect = Exception("Database error")

                # Act & Assert
                with pytest.raises(Exception):
                    get_current_user(mock_credentials, db_session)

