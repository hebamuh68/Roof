import pytest
from sqlalchemy import create_engine, event, JSON, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import sqlite
from sqlalchemy.dialects.postgresql import ARRAY
from app.database.database import Base
from tests.factories.apartment_factory import ApartmentFactory

# Import all models to register them with Base metadata
from app.schemas.user_sql import UserDB
from app.schemas.apartment_sql import ApartmentDB
from app.schemas.password_reset_sql import PasswordResetTokenDB
from app.schemas.message_sql import MessageDB
from app.schemas.notifications_sql import NotificationDB

# Setup test DB (you can use SQLite for speed)
TEST_DATABASE_URL = "sqlite:///./test.db"

# Override ARRAY type for SQLite (use JSON instead since SQLite doesn't support ARRAY)
@event.listens_for(Base.metadata, "before_create")
def receive_before_create(target, connection, **kw):
    """Replace PostgreSQL ARRAY with JSON for SQLite"""
    if connection.dialect.name == "sqlite":
        for table in target.tables.values():
            for column in table.columns:
                if isinstance(column.type, ARRAY):
                    # Replace ARRAY with JSON for SQLite
                    column.type = JSON()

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture
def apartment_factory(db_session):
    def _make(**kwargs):
        return ApartmentFactory.build(session=db_session, **kwargs)
    return _make


def user_factory(db_session, email: str, first_name: str = "Test", last_name: str = "User", role: str = "SEEKER", location: str = "Sydney"):
    """Factory function to create test users"""
    from app.schemas.user_sql import UserDB, UserType

    user = UserDB(
        email=email,
        first_name=first_name,
        last_name=last_name,
        location=location,
        hashed_password="hashed_password_placeholder",
        role=UserType(role) if isinstance(role, str) else role
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user