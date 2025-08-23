from datetime import datetime
from app.database.database import SessionLocal
from app.schemas.user_sql import UserDB
from app.schemas.apartment_sql import ApartmentDB

def seed():
    db = SessionLocal()
    try:
        # Users
        users = [
            User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                location="Cairo",
                flatmate_pref=["Non-smoker", "Pet friendly"],
                keywords=["friendly", "quiet"]
            ),
            User(
                first_name="Jane",
                last_name="Smith",
                email="jane@example.com",
                location="Giza",
                flatmate_pref=["Female only"],
                keywords=["clean", "student"]
            ),
        ]

        # Apartments
        apartments = [
            Apartment(
                title="Sunny Apartment in Downtown",
                description="A cozy 2-bedroom apartment with great lighting.",
                location="Cairo",
                apartment_type="2BHK",
                rent_per_week=1250,
                start_date=datetime(2025, 9, 1, 12, 0),
                duration_len=12,
                place_accept="Both",
                furnishing_type="Furnished",
                is_pathroom_solo=True,
                parking_type="Street",
                keywords=["WiFi", "AC", "Washing Machine"],
                is_active=True
            ),
            Apartment(
                title="Shared Flat in Giza",
                description="Looking for a flatmate, close to university.",
                location="Giza",
                apartment_type="Shared",
                rent_per_week=750,
                start_date=datetime(2025, 8, 20, 12, 0),
                duration_len=6,
                place_accept="Female",
                furnishing_type="Semi-furnished",
                is_pathroom_solo=False,
                parking_type="None",
                keywords=["Balcony", "Near Metro"],
                is_active=True
            ),
            Apartment(
                title="Modern Studio in Maadi",
                description="Fully furnished studio with balcony and parking.",
                location="Maadi",
                apartment_type="Studio",
                rent_per_week=900,
                start_date=datetime(2025, 10, 1, 12, 0),
                duration_len=6,
                place_accept="Both",
                furnishing_type="Furnished",
                is_pathroom_solo=True,
                parking_type="Private",
                keywords=["Balcony", "Parking", "Furnished"],
                is_active=True
            ),
        ]

        db.add_all(users + apartments)
        db.commit()
        print("✅ Data seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
