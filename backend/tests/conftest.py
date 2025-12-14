import pytest
from sqlalchemy import create_engine, event, JSON, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import sqlite
from sqlalchemy.dialects.postgresql import ARRAY
from app.database.database import Base
from tests.factories.apartment_factory import ApartmentFactory

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