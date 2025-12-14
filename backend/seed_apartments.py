#!/usr/bin/env python3
"""
Apartment Database Seeding Script

This script populates the database with sample apartment data for development
and testing purposes. It creates both users and apartments with realistic
randomized data.

Usage:
    python seed_apartments.py

Features:
    - Creates sample users if none exist
    - Generates 50 realistic apartment listings
    - Randomizes all apartment properties
    - Creates relationships between apartments and users
    - Provides detailed progress output

Note:
    This script should only be used in development environments.
    Do not run in production as it creates sample data.
"""

import random
from datetime import datetime, timedelta, timezone

from app.database.database import SessionLocal
from app.schemas.user_sql import UserDB, UserType
from app.schemas.apartment_sql import ApartmentDB
from app.utils.auth import get_password_hash


# ===========================
# Sample Data Constants
# ===========================

LOCATIONS = [
    "Cairo", "Giza", "Maadi", "Zamalek", "Heliopolis",
    "New Cairo", "Nasr City", "6th October", "Sheikh Zayed", "Dokki"
]

APARTMENT_TYPES = [
    "Studio", "1BHK", "2BHK", "3BHK", "4BHK", "Shared", "Penthouse"
]

FURNISHING_TYPES = [
    "Furnished", "Semi-furnished", "Unfurnished"
]

PARKING_TYPES = [
    "Private", "Street", "Garage", "None"
]

PLACE_ACCEPT = [
    "Both", "Male", "Female"
]

# Sample image URLs (placeholder - replace with actual image URLs in production)
SAMPLE_IMAGE_URLS = [
    "/static/images/sample1.jpg",
    "/static/images/sample2.jpg",
    "/static/images/sample3.jpg",
    "/static/images/sample4.jpg",
    "/static/images/sample5.jpg",
    "/static/images/sample6.jpg",
]

# Apartment title templates
TITLES = [
    "Cozy Studio Apartment", "Modern 2-Bedroom Flat", "Spacious 3-Bedroom Apartment",
    "Luxury Penthouse", "Shared Room Available", "Furnished Studio",
    "Bright 1-Bedroom Apartment", "Family-Friendly 4-Bedroom", "Student-Friendly Shared Space",
    "Downtown Apartment", "Quiet Residential Unit", "City Center Location",
    "Near Metro Station", "Garden View Apartment", "Rooftop Access",
    "Pet-Friendly Space", "Newly Renovated", "High-Speed Internet Included",
    "AC and Heating", "Fully Equipped Kitchen", "Walking Distance to University",
    "Shopping Mall Nearby", "Parking Available", "Security Building",
    "Elevator Access", "Balcony Included", "Swimming Pool Access",
    "Gym Facilities", "24/7 Security", "Prime Location"
]

DESCRIPTIONS = [
    "Beautiful apartment with modern amenities and great location.",
    "Spacious and well-maintained property perfect for families or professionals.",
    "Recently renovated with high-quality finishes throughout.",
    "Close to public transportation and major shopping areas.",
    "Quiet neighborhood with easy access to city center.",
    "Fully furnished with all necessary appliances included.",
    "Great natural light and ventilation throughout.",
    "Ideal for students or young professionals.",
    "Pet-friendly building with nearby parks.",
    "Secure building with 24/7 security and CCTV.",
    "Walking distance to restaurants, cafes, and entertainment.",
    "Well-connected area with excellent public transport links.",
    "Modern kitchen with all appliances, perfect for cooking enthusiasts.",
    "Comfortable living space with separate bedrooms for privacy.",
    "Great investment opportunity in a growing neighborhood."
]

KEYWORDS_OPTIONS = [
    ["WiFi", "AC", "Furnished"],
    ["Parking", "Balcony", "Elevator"],
    ["Near Metro", "Shopping", "Restaurants"],
    ["Security", "CCTV", "24/7"],
    ["Pet Friendly", "Gym", "Pool"],
    ["Student Friendly", "Quiet", "Study Area"],
    ["Modern", "Renovated", "New"],
    ["Family Friendly", "Safe", "Schools Nearby"],
    ["Furnished", "Appliances", "Ready to Move"],
    ["Downtown", "City Center", "Prime Location"]
]


# ===========================
# Helper Functions
# ===========================

def get_or_create_users(db: SessionLocal) -> list[UserDB]:
    """
    Get existing users or create sample users if none exist.

    This ensures there are users available to assign as apartment owners.

    Args:
        db: Database session

    Returns:
        list[UserDB]: List of user objects

    Note:
        Creates 5 sample users with Egyptian names and realistic data.
    """
    users = db.query(UserDB).all()

    if not users:
        print("No users found. Creating sample users...")
        sample_users = [
            UserDB(
                first_name="Ahmed",
                last_name="Ali",
                email="ahmed.ali@example.com",
                location="Cairo",
                flatmate_pref=["Non-smoker"],
                keywords=["friendly", "clean"],
                role=UserType.RENTER,
                hashed_password=get_password_hash("password123")
            ),
            UserDB(
                first_name="Sarah",
                last_name="Mohamed",
                email="sarah.mohamed@example.com",
                location="Giza",
                flatmate_pref=["Female only", "Pet friendly"],
                keywords=["quiet", "student"],
                role=UserType.RENTER,
                hashed_password=get_password_hash("password123")
            ),
            UserDB(
                first_name="Mohamed",
                last_name="Hassan",
                email="mohamed.hassan@example.com",
                location="Maadi",
                flatmate_pref=["Professional"],
                keywords=["clean", "organized"],
                role=UserType.RENTER,
                hashed_password=get_password_hash("password123")
            ),
            UserDB(
                first_name="Fatima",
                last_name="Ibrahim",
                email="fatima.ibrahim@example.com",
                location="Zamalek",
                flatmate_pref=["Non-smoker", "Quiet"],
                keywords=["friendly", "respectful"],
                role=UserType.RENTER,
                hashed_password=get_password_hash("password123")
            ),
            UserDB(
                first_name="Omar",
                last_name="Khalil",
                email="omar.khalil@example.com",
                location="Heliopolis",
                flatmate_pref=["Male", "Student"],
                keywords=["study", "quiet"],
                role=UserType.RENTER,
                hashed_password=get_password_hash("password123")
            ),
        ]
        db.add_all(sample_users)
        db.commit()
        for user in sample_users:
            db.refresh(user)
        users = sample_users
        print(f"✅ Created {len(users)} users")

    return users


def calculate_rent_by_type(apartment_type: str) -> int:
    """
    Calculate realistic rent based on apartment type.

    Args:
        apartment_type: Type of apartment (Studio, 1BHK, etc.)

    Returns:
        int: Weekly rent amount in currency units
    """
    rent_ranges = {
        "Studio": (600, 1200),
        "1BHK": (800, 1500),
        "2BHK": (1200, 2500),
        "3BHK": (1800, 3500),
        "4BHK": (2500, 5000),
        "Shared": (400, 800),
        "Penthouse": (3000, 6000),
    }

    min_rent, max_rent = rent_ranges.get(apartment_type, (600, 2000))
    return random.randint(min_rent, max_rent)


# ===========================
# Main Seeding Function
# ===========================

def generate_apartments(count: int = 50) -> None:
    """
    Generate and insert apartment seed data into the database.

    Creates realistic apartment listings with randomized properties,
    assigns them to existing users, and provides detailed output.

    Args:
        count: Number of apartments to create (default: 50)

    Raises:
        Exception: If database operation fails, rolls back and prints error
    """
    db = SessionLocal()
    try:
        # Ensure we have users to assign apartments to
        users = get_or_create_users(db)
        if not users:
            print("❌ No users available. Cannot create apartments.")
            return

        apartments = []
        base_date = datetime.now(timezone.utc)

        for i in range(count):
            # Randomize apartment properties
            location = random.choice(LOCATIONS)
            apartment_type = random.choice(APARTMENT_TYPES)
            furnishing = random.choice(FURNISHING_TYPES)
            parking = random.choice(PARKING_TYPES)
            place_accept = random.choice(PLACE_ACCEPT)

            # Calculate appropriate rent
            rent = calculate_rent_by_type(apartment_type)

            # Random start date (within next 3 months)
            days_ahead = random.randint(0, 90)
            start_date = base_date + timedelta(days=days_ahead)

            # Duration (3, 6, 12 months or None)
            duration_options = [3, 6, 12, None]
            duration = random.choice(duration_options)

            # Generate 4-6 random image URLs
            num_images = random.randint(4, 6)
            images = random.sample(
                SAMPLE_IMAGE_URLS,
                min(num_images, len(SAMPLE_IMAGE_URLS))
            )

            # Compose title and description
            title = f"{random.choice(TITLES)} in {location}"
            description = random.choice(DESCRIPTIONS)

            # Select keywords
            keywords = random.choice(KEYWORDS_OPTIONS)

            # Assign to random user
            renter = random.choice(users)

            # Create apartment instance
            apartment = ApartmentDB(
                title=title,
                description=description,
                location=location,
                apartment_type=apartment_type,
                rent_per_week=rent,
                start_date=start_date,
                duration_len=duration,
                place_accept=place_accept,
                furnishing_type=furnishing,
                is_pathroom_solo=random.choice([True, False]),
                parking_type=parking,
                keywords=keywords,
                images=images,
                is_active=random.choice([True, True, True, False]),  # 75% active
                renter_id=renter.id
            )
            apartments.append(apartment)

        # Bulk insert all apartments
        db.add_all(apartments)
        db.commit()

        # Print summary
        print(f"✅ Successfully seeded {count} apartments!")
        print(f"   - Locations: {', '.join(set(apt.location for apt in apartments))}")
        print(f"   - Active apartments: {sum(1 for apt in apartments if apt.is_active)}")
        print(f"   - Inactive apartments: {sum(1 for apt in apartments if not apt.is_active)}")
        print(f"   - Apartment types: {', '.join(set(apt.apartment_type for apt in apartments))}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding apartments: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


# ===========================
# Script Entry Point
# ===========================

if __name__ == "__main__":
    print("🌱 Starting apartment seeding...")
    print("=" * 50)
    generate_apartments(50)
    print("=" * 50)
    print("✨ Done!")
