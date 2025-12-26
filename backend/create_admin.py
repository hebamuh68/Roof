#!/usr/bin/env python3
"""
Script to create an admin user
Usage: python create_admin.py <email> <password> <first_name> <last_name> <location>
"""
import sys
from app.database.database import SessionLocal
# Import ApartmentDB first to resolve the relationship
from app.schemas.apartment_sql import ApartmentDB
from app.schemas.user_sql import UserDB, UserType
from app.utils.auth import get_password_hash

def create_admin_user(email: str, password: str, first_name: str, last_name: str, location: str = "Cairo"):
    """Create an admin user in the database"""
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(UserDB).filter(UserDB.email == email).first()
        if existing_user:
            print(f"❌ User with email {email} already exists!")
            if existing_user.role == UserType.ADMIN:
                print(f"   User is already an admin.")
            else:
                print(f"   Current role: {existing_user.role.value}")
                response = input("   Do you want to update this user to admin? (y/n): ")
                if response.lower() == 'y':
                    existing_user.role = UserType.ADMIN
                    existing_user.hashed_password = get_password_hash(password)
                    db.commit()
                    print(f"✅ User {email} updated to admin!")
                    return
            return

        # Create new admin user
        admin_user = UserDB(
            first_name=first_name,
            last_name=last_name,
            email=email,
            location=location,
            role=UserType.ADMIN,
            hashed_password=get_password_hash(password),
            flatmate_pref=[],
            keywords=[]
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✅ Admin user created successfully!")
        print(f"   Email: {email}")
        print(f"   Name: {first_name} {last_name}")
        print(f"   Location: {location}")
        print(f"   Role: ADMIN")
        print(f"\n   You can now login at /login with:")
        print(f"   Email: {email}")
        print(f"   Password: {password}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python create_admin.py <email> <password> <first_name> <last_name> <location>")
        print("\nExample:")
        print("  python create_admin.py admin@roof.com admin123 Admin User Cairo")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    first_name = sys.argv[3]
    last_name = sys.argv[4]
    location = sys.argv[5] if len(sys.argv) > 5 else "Cairo"
    
    create_admin_user(email, password, first_name, last_name, location)

