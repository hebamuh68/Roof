"""
Apartment Service Layer

This module contains the business logic for apartment operations.
Acts as an intermediary between the API layer and the database layer.

Responsibilities:
- Data transformation (API input → Database models)
- Business rule enforcement
- Image handling and validation
- Database transaction management
- Error handling with cleanup on failures

Functions:
    create_apartment: Create new apartment with image uploads
    get_apartment_by_id: Retrieve apartment by ID
    get_my_apartments: Get apartments owned by specific user
    get_my_apartments_count: Count user's apartments
    list_apartments: List all apartments with pagination
    update_apartment: Update existing apartment
    delete_apartment: Delete apartment and associated images
"""

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from typing import List
from pathlib import Path
from datetime import datetime

from app.schemas.apartment_sql import ApartmentDB
from app.models.apartment_pyd import ApartmentRequest, ApartmentFilter, ApartmentCreateInput
from app.utils.image_upload import save_multiple_images, get_image_url, delete_image_file


# ===========================
# Create Operations
# ===========================

async def create_apartment(
    db: Session,
    apartment_input: ApartmentCreateInput,
    images: List[UploadFile]
) -> ApartmentDB:
    """
    Create a new apartment listing with image uploads.

    This function handles the complete apartment creation workflow:
    1. Save uploaded images to filesystem
    2. Parse and validate date strings
    3. Transform comma-separated keywords to list
    4. Validate all data with Pydantic
    5. Create database record
    6. Automatic cleanup on any failure

    Args:
        db: Database session
        apartment_input: Validated input data from API
        images: List of uploaded image files (minimum 4 required)

    Returns:
        ApartmentDB: Created apartment database object

    Raises:
        HTTPException 400: Image save failed, date parsing failed, or validation error
        HTTPException 500: Database operation failed

    Note:
        All images are automatically deleted from filesystem if any step fails,
        ensuring no orphaned files.
    """
    saved_filenames = []

    # Step 1: Save images to filesystem
    try:
        saved_filenames = await save_multiple_images(images)
        image_urls = [get_image_url(filename) for filename in saved_filenames]
    except Exception as e:
        # Clean up any partially saved images
        for filename in saved_filenames:
            delete_image_file(filename)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to save images: {str(e)}"
        )

    # Step 2: Parse start_date from ISO format string to datetime
    try:
        # Handle both 'Z' and '+00:00' timezone formats
        parsed_start_date = datetime.fromisoformat(
            apartment_input.start_date.replace('Z', '+00:00')
        )
    except ValueError as e:
        # Clean up images if date parsing fails
        for filename in saved_filenames:
            delete_image_file(filename)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid start_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS): {str(e)}"
        )

    # Step 3: Parse keywords from comma-separated string to list
    keywords_list = None
    if apartment_input.keywords:
        keywords_list = [
            k.strip()
            for k in apartment_input.keywords.split(",")
            if k.strip()
        ]

    # Step 4: Create validated ApartmentRequest object
    # Pydantic will validate minimum 4 images and all other constraints
    try:
        apartment_data = ApartmentRequest(
            images=image_urls,
            title=apartment_input.title,
            description=apartment_input.description,
            location=apartment_input.location,
            apartment_type=apartment_input.apartment_type,
            rent_per_week=apartment_input.rent_per_week,
            start_date=parsed_start_date,
            duration_len=apartment_input.duration_len,
            place_accept=apartment_input.place_accept,
            furnishing_type=apartment_input.furnishing_type,
            is_pathroom_solo=apartment_input.is_pathroom_solo,
            parking_type=apartment_input.parking_type,
            keywords=keywords_list,
            is_active=apartment_input.is_active,
            renter_id=apartment_input.renter_id
        )
    except Exception as e:
        # Clean up images if validation fails
        for filename in saved_filenames:
            delete_image_file(filename)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )

    # Step 5: Convert Pydantic model to SQLAlchemy model and save to database
    db_apartment = ApartmentDB(**apartment_data.model_dump())
    db.add(db_apartment)

    try:
        db.commit()
        db.refresh(db_apartment)
        return db_apartment
    except Exception as e:
        db.rollback()
        # Clean up images if database operation fails
        for filename in saved_filenames:
            delete_image_file(filename)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create apartment: {str(e)}"
        )


# ===========================
# Read Operations
# ===========================

def get_apartment_by_id(db: Session, apartment_id: int) -> ApartmentDB | None:
    """
    Retrieve a single apartment by its unique ID.

    Args:
        db: Database session
        apartment_id: Unique identifier of the apartment

    Returns:
        ApartmentDB: Found apartment object, or None if not found
    """
    return db.query(ApartmentDB)\
        .filter(ApartmentDB.id == apartment_id)\
        .first()


def get_my_apartments(
    db: Session,
    renter_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[ApartmentDB]:
    """
    Get all apartments owned by a specific user.

    Returns apartments ordered by creation date (newest first).
    Supports pagination for large result sets.

    Args:
        db: Database session
        renter_id: User ID of the apartment owner
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return

    Returns:
        List[ApartmentDB]: List of apartment objects owned by the user

    Example:
        # Get first page (20 items)
        page1 = get_my_apartments(db, user_id=5, skip=0, limit=20)

        # Get second page
        page2 = get_my_apartments(db, user_id=5, skip=20, limit=20)
    """
    return db.query(ApartmentDB)\
        .filter(ApartmentDB.renter_id == renter_id)\
        .order_by(ApartmentDB.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_my_apartments_count(db: Session, renter_id: int) -> int:
    """
    Get total count of apartments owned by a specific user.

    Useful for pagination - calculate total pages and display counts.

    Args:
        db: Database session
        renter_id: User ID of the apartment owner

    Returns:
        int: Total number of apartments owned by the user
    """
    return db.query(ApartmentDB)\
        .filter(ApartmentDB.renter_id == renter_id)\
        .count()


def list_apartments(
    db: Session,
    skip: int = 0,
    limit: int = 10
) -> List[ApartmentDB]:
    """
    List all apartments with pagination.

    Returns apartments in reverse chronological order (newest first).
    Public endpoint - returns all active apartments.

    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return

    Returns:
        List[ApartmentDB]: List of apartment objects

    Todo:
        - Add filtering by status (active/inactive)
        - Add sorting options
        - Add search functionality
    """
    return db.query(ApartmentDB)\
        .order_by(ApartmentDB.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()


# ===========================
# Update Operations
# ===========================

def update_apartment(
    db: Session,
    apartment_id: int,
    apartment_data: ApartmentFilter
) -> ApartmentDB | None:
    """
    Update an existing apartment with partial data.

    Supports partial updates - only provided fields will be modified.
    Automatically updates the updated_at timestamp.

    Args:
        db: Database session
        apartment_id: ID of apartment to update
        apartment_data: Filter object containing fields to update

    Returns:
        ApartmentDB: Updated apartment object, or None if not found

    Example:
        # Update only title and rent
        filter_data = ApartmentFilter(title="New Title", rent_per_week=1500)
        updated = update_apartment(db, apartment_id=5, apartment_data=filter_data)

    Note:
        Ownership validation should be performed in the API layer
        before calling this function.
    """
    db_apartment = db.query(ApartmentDB)\
        .filter(ApartmentDB.id == apartment_id)\
        .first()

    if not db_apartment:
        return None

    # Extract only the fields that were actually provided
    apartment_clean = apartment_data.model_dump(exclude_unset=True)

    # Update each provided field
    for field, value in apartment_clean.items():
        setattr(db_apartment, field, value)

    db.commit()
    db.refresh(db_apartment)
    return db_apartment


# ===========================
# Delete Operations
# ===========================

def delete_apartment(db: Session, apartment_id: int) -> dict | None:
    """
    Delete an apartment and all associated images.

    Performs complete cleanup:
    1. Deletes all images from filesystem
    2. Deletes database record

    Args:
        db: Database session
        apartment_id: ID of apartment to delete

    Returns:
        dict: Success message, or None if apartment not found

    Note:
        This operation is irreversible. Ownership validation should
        be performed in the API layer before calling this function.

    Example:
        result = delete_apartment(db, apartment_id=5)
        if result:
            print("Deleted successfully")
        else:
            print("Apartment not found")
    """
    db_apartment = db.query(ApartmentDB)\
        .filter(ApartmentDB.id == apartment_id)\
        .first()

    if not db_apartment:
        return None

    # Delete associated images from filesystem
    if db_apartment.images:
        for image_url in db_apartment.images:
            # Extract filename from URL
            # Example: /static/images/filename.jpg -> filename.jpg
            filename = Path(image_url).name
            delete_image_file(filename)

    # Delete the apartment record
    db.delete(db_apartment)
    db.commit()

    return {"message": "Apartment deleted successfully"}
