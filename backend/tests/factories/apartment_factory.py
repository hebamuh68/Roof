"""
Apartment Test Data Factory

This module provides a Factory Boy factory for generating test apartment data.
Used in unit and integration tests to create realistic apartment instances
with randomized but valid data.

Usage:
    # Create and save to database
    apartment = ApartmentFactory.create()

    # Build without saving
    apartment = ApartmentFactory.build()

    # Create with specific values
    apartment = ApartmentFactory.create(title="Custom Title", rent_per_week=1500)

    # Create multiple
    apartments = ApartmentFactory.create_batch(5)
"""

import factory
from datetime import datetime, timedelta, timezone

from app.schemas.apartment_sql import ApartmentDB


class ApartmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Factory for generating ApartmentDB test instances.

    Generates realistic apartment data using Faker for randomization.
    All required fields are populated with sensible defaults.

    Attributes:
        title: Random 3-word sentence
        description: Random paragraph
        location: Random city name
        apartment_type: Cycles through Studio, 1BHK, 2BHK
        rent_per_week: Random integer between 100 and 2000
        start_date: Tomorrow's date (UTC)
        duration_len: Random weeks between 1 and 52
        place_accept: Cycles through tenant types
        furnishing_type: Cycles through furnishing options
        is_pathroom_solo: Random boolean
        parking_type: Cycles through parking options
        keywords: Default list of amenities
        is_active: Always True
        renter_id: Random integer 1-10 (should be overridden in tests)

    Example:
        ```python
        # In a test
        def test_something(db_session):
            apartment = ApartmentFactory.create(
                session=db_session,
                title="Test Apartment",
                rent_per_week=1000
            )
            assert apartment.id is not None
        ```
    """

    class Meta:
        model = ApartmentDB
        sqlalchemy_session_persistence = "commit"

    # Basic Information
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    location = factory.Faker("city")

    # Classification
    apartment_type = factory.Iterator(["Studio", "1BHK", "2BHK", "3BHK"])

    # Pricing & Availability
    rent_per_week = factory.Faker("random_int", min=100, max=2000)
    start_date = factory.LazyFunction(
        lambda: datetime.now(timezone.utc) + timedelta(days=1)
    )
    duration_len = factory.Faker("random_int", min=1, max=52)

    # Tenant Preferences
    place_accept = factory.Iterator(["Students", "Professionals", "Families", "Both"])

    # Property Details
    furnishing_type = factory.Iterator(["Furnished", "Unfurnished", "Semi-Furnished"])
    is_pathroom_solo = factory.Faker("boolean")
    parking_type = factory.Iterator(["Garage", "Street", "Private", "None"])

    # Amenities
    keywords = ["wifi", "balcony", "central heating"]

    # Status
    is_active = True

    # Relationships
    # Note: In real tests, this should be set to an actual user ID
    renter_id = factory.Faker("random_int", min=1, max=10)
