"""
Apartment SQLAlchemy ORM Model

This module defines the SQLAlchemy ORM model for the apartments table.
Represents the database schema and handles the mapping between Python
objects and database rows.

Database Table: apartments
Primary Relationships:
    - Many-to-One with UserDB (renter)
"""

from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone

from app.database.database import Base


class ApartmentDB(Base):
    """
    Apartment database model (ORM).

    Represents an apartment listing in the database with all its properties,
    relationships, and metadata.

    Table: apartments

    Columns:
        id: Primary key, unique identifier
        images: Array of image URLs/paths (PostgreSQL ARRAY)
        title: Apartment title/name
        description: Detailed text description
        location: Physical address or location string
        apartment_type: Type classification (Studio, 1BHK, etc.)
        rent_per_week: Weekly rental cost in currency units
        start_date: Date when apartment becomes available
        duration_len: Rental period duration in weeks (optional)
        place_accept: Accepted tenant type (Students, Professionals, Both)
        furnishing_type: Furnishing status (Furnished, Semi-Furnished, Unfurnished)
        is_pathroom_solo: True if private bathroom, False if shared
        parking_type: Parking availability (Private, Street, Garage, None)
        keywords: Array of amenity/feature strings (PostgreSQL ARRAY)
        is_active: Whether listing is currently active
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
        renter_id: Foreign key to users table (apartment owner)

    Relationships:
        renter: Many-to-One relationship with UserDB
                Access owner info via apartment.renter.first_name, etc.

    Indexes:
        - Primary key index on id
        - Foreign key on renter_id

    Constraints:
        - NOT NULL: title, location, apartment_type, rent_per_week, start_date,
                    place_accept, furnishing_type, is_pathroom_solo, parking_type,
                    is_active, created_at, updated_at
        - Foreign Key: renter_id references users(id)

    Example Usage:
        # Create new apartment
        apartment = ApartmentDB(
            title="Cozy Studio",
            location="Downtown",
            apartment_type="Studio",
            rent_per_week=500,
            start_date=datetime.now(),
            place_accept="Both",
            furnishing_type="Furnished",
            is_pathroom_solo=True,
            parking_type="Street",
            is_active=True,
            renter_id=user.id
        )
        db.add(apartment)
        db.commit()

        # Query with relationship
        apartment = db.query(ApartmentDB).filter_by(id=1).first()
        owner_name = f"{apartment.renter.first_name} {apartment.renter.last_name}"
    """

    __tablename__ = "apartments"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique apartment identifier"
    )

    # Media
    images = Column(
        ARRAY(String),
        nullable=True,
        comment="Array of image URLs/paths"
    )

    # Basic Information
    title = Column(
        String,
        nullable=False,
        comment="Apartment title/name"
    )

    description = Column(
        Text,
        nullable=True,
        comment="Detailed description"
    )

    location = Column(
        String,
        nullable=False,
        comment="Physical address or location"
    )

    apartment_type = Column(
        String,
        nullable=False,
        comment="Type (Studio, 1BHK, 2BHK, etc.)"
    )

    # Pricing & Availability
    rent_per_week = Column(
        Integer,
        nullable=False,
        comment="Weekly rental cost"
    )

    start_date = Column(
        DateTime,
        nullable=False,
        comment="Availability start date"
    )

    duration_len = Column(
        Integer,
        nullable=True,
        comment="Rental duration in weeks"
    )

    # Tenant Preferences
    place_accept = Column(
        String,
        nullable=False,
        comment="Accepted tenant type (Students/Professionals/Both)"
    )

    # Property Details
    furnishing_type = Column(
        String,
        nullable=False,
        comment="Furnishing status (Furnished/Semi-Furnished/Unfurnished)"
    )

    is_pathroom_solo = Column(
        Boolean,
        nullable=False,
        comment="True=Private bathroom, False=Shared"
    )

    parking_type = Column(
        String,
        nullable=False,
        comment="Parking type (Private/Street/Garage/None)"
    )

    keywords = Column(
        ARRAY(String),
        nullable=True,
        comment="Array of amenity/feature tags"
    )

    # Status
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Listing active status"
    )

    # Timestamps
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="Record creation timestamp"
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="Last update timestamp"
    )

    # Foreign Keys & Relationships
    renter_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        comment="Foreign key to users table (apartment owner)"
    )

    renter = relationship(
        "UserDB",
        back_populates="apartments",
        doc="Relationship to apartment owner (UserDB)"
    )

    def __repr__(self) -> str:
        """String representation of ApartmentDB instance."""
        return (
            f"<ApartmentDB(id={self.id}, "
            f"title='{self.title}', "
            f"location='{self.location}', "
            f"type='{self.apartment_type}', "
            f"rent={self.rent_per_week})>"
        )
