#!/usr/bin/env python3
"""
Script to create an admin user
Usage: python create_admin.py <email> <password> <first_name> <last_name>
"""
import sys
from app.database.database import SessionLocal
from app.schemas.user_sql import UserDB
from app.schemas.property_sql import PropertyDB  # noqa: F401
from app.schemas.property_image_sql import PropertyImageDB  # noqa: F401
from app.schemas.review_sql import ReviewDB  # noqa: F401
from app.schemas.message_sql import MessageDB  # noqa: F401
from app.schemas.notifications_sql import NotificationDB  # noqa: F401
from app.utils.auth import get_password_hash


def create_admin_user(email: str, password: str, first_name: str, last_name: str):
    db = SessionLocal()
    try:
        existing_user = db.query(UserDB).filter(UserDB.email == email).first()
        if existing_user:
            print(f"User with email {email} already exists!")
            if existing_user.is_admin:
                print("   User is already an admin.")
            else:
                response = input("   Do you want to update this user to admin? (y/n): ")
                if response.lower() == "y":
                    existing_user.is_admin = True
                    existing_user.hashed_password = get_password_hash(password)
                    db.commit()
                    print(f"User {email} updated to admin!")
            return

        admin_user = UserDB(
            email=email,
            hashed_password=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            is_admin=True,
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"Admin user created successfully!")
        print(f"   Email: {email}")
        print(f"   Name: {first_name} {last_name}")

    except Exception as e:
        db.rollback()
        print(f"Error creating admin user: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python create_admin.py <email> <password> <first_name> <last_name>")
        print("\nExample:")
        print("  python create_admin.py admin@roof.com admin123 Admin User")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    first_name = sys.argv[3]
    last_name = sys.argv[4]

    create_admin_user(email, password, first_name, last_name)
