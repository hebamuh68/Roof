import pytest
from sqlalchemy.orm import Session
from app.services.user_service import update_user, block_user
from app.models.user_pyd import UserUpdate
from app.schemas.user_sql import UserDB, UserType
from tests.conftest import user_factory


class TestUserService:
    """Test suite for user service operations."""

    def test_update_user_success(self, db_session: Session):
        """Test successful user update with valid data."""
        # Arrange
        user = user_factory(
            db_session,
            email="update@test.com",
            first_name="John",
            last_name="Doe",
            location="Sydney"
        )

        user_update = UserUpdate(
            first_name="Jane",
            last_name="Smith",
            location="Melbourne"
        )

        # Act
        updated_user = update_user(db_session, user.id, user_update)

        # Assert
        assert updated_user is not None
        assert updated_user.id == user.id
        assert updated_user.first_name == "Jane"
        assert updated_user.last_name == "Smith"
        assert updated_user.location == "Melbourne"
        assert updated_user.email == "update@test.com"  # Email unchanged

    def test_update_user_partial(self, db_session: Session):
        """Test updating only some fields."""
        # Arrange
        user = user_factory(
            db_session,
            email="partial@test.com",
            first_name="John",
            last_name="Doe",
            location="Sydney"
        )

        user_update = UserUpdate(first_name="Jane")

        # Act
        updated_user = update_user(db_session, user.id, user_update)

        # Assert
        assert updated_user.first_name == "Jane"
        assert updated_user.last_name == "Doe"  # Unchanged
        assert updated_user.location == "Sydney"  # Unchanged

    def test_update_user_password(self, db_session: Session):
        """Test updating user password (should be hashed)."""
        # Arrange
        user = user_factory(db_session, email="password@test.com")
        original_password = user.hashed_password

        user_update = UserUpdate(password="NewSecurePassword123!")

        # Act
        updated_user = update_user(db_session, user.id, user_update)

        # Assert
        assert updated_user.hashed_password != original_password
        assert updated_user.hashed_password != "NewSecurePassword123!"  # Should be hashed
        assert len(updated_user.hashed_password) > 20  # Bcrypt hash is long

    def test_update_user_role(self, db_session: Session):
        """Test updating user role."""
        # Arrange
        user = user_factory(
            db_session,
            email="role@test.com",
            role="SEEKER"
        )

        user_update = UserUpdate(role="RENTER")

        # Act
        updated_user = update_user(db_session, user.id, user_update)

        # Assert
        assert updated_user.role == UserType.RENTER

    def test_update_user_not_found(self, db_session: Session):
        """Test updating non-existent user returns None."""
        # Arrange
        user_update = UserUpdate(first_name="Jane")

        # Act
        result = update_user(db_session, 99999, user_update)

        # Assert
        assert result is None

    def test_update_user_empty_update(self, db_session: Session):
        """Test updating with empty update (no changes)."""
        # Arrange
        user = user_factory(
            db_session,
            email="empty@test.com",
            first_name="John"
        )

        user_update = UserUpdate()

        # Act
        updated_user = update_user(db_session, user.id, user_update)

        # Assert
        assert updated_user is not None
        assert updated_user.first_name == "John"  # Unchanged

    def test_block_user_success(self, db_session: Session):
        """Test successful user blocking (deletion)."""
        # Arrange
        user = user_factory(db_session, email="block@test.com")

        # Act
        result = block_user(db_session, user.id)

        # Assert
        assert result is not None
        assert result["message"] == "User blocked successfully"

        # Verify user is deleted
        deleted_user = db_session.query(UserDB).filter(UserDB.id == user.id).first()
        assert deleted_user is None

    def test_block_user_not_found(self, db_session: Session):
        """Test blocking non-existent user returns None."""
        # Act
        result = block_user(db_session, 99999)

        # Assert
        assert result is None

    def test_update_user_multiple_fields(self, db_session: Session):
        """Test updating multiple fields at once."""
        # Arrange
        user = user_factory(
            db_session,
            email="multi@test.com",
            first_name="John",
            last_name="Doe",
            location="Sydney"
        )

        user_update = UserUpdate(
            first_name="Jane",
            last_name="Smith",
            location="Melbourne",
            role="RENTER"
        )

        # Act
        updated_user = update_user(db_session, user.id, user_update)

        # Assert
        assert updated_user.first_name == "Jane"
        assert updated_user.last_name == "Smith"
        assert updated_user.location == "Melbourne"
        assert updated_user.role == UserType.RENTER

    def test_update_user_with_keywords(self, db_session: Session):
        """Test updating user with keywords array."""
        # Arrange
        user = user_factory(db_session, email="keywords@test.com")

        user_update = UserUpdate(
            keywords=["pet-friendly", "quiet", "near-transit"]
        )

        # Act
        updated_user = update_user(db_session, user.id, user_update)

        # Assert
        assert updated_user.keywords == ["pet-friendly", "quiet", "near-transit"]

    def test_update_user_with_flatmate_preferences(self, db_session: Session):
        """Test updating user with flatmate preferences."""
        # Arrange
        user = user_factory(db_session, email="flatmate@test.com")

        user_update = UserUpdate(
            flatmate_preferences=["non-smoker", "clean", "professional"]
        )

        # Act
        updated_user = update_user(db_session, user.id, user_update)

        # Assert
        assert updated_user.flatmate_preferences == ["non-smoker", "clean", "professional"]

