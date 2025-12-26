from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

DATABASE_URL = os.getenv("DATABASE_URL")

# Handle Render's postgres:// URL format (needs postgresql://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Default to SQLite for local development
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()