#!/usr/bin/env python3
"""
Simple script to create database tables
"""
from app.database.database import engine, Base
from app.schemas.user_sql import UserDB
from app.schemas.apartment_sql import ApartmentDB

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
