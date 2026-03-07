#!/usr/bin/env python3
"""
Script to create all database tables for the roof-enums schema.
"""
from app.database.database import engine, Base
from app.schemas.user_sql import UserDB
from app.schemas.property_sql import PropertyDB
from app.schemas.property_image_sql import PropertyImageDB
from app.schemas.review_sql import ReviewDB
from app.schemas.message_sql import MessageDB
from app.schemas.notifications_sql import NotificationDB


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")


if __name__ == "__main__":
    create_tables()
