"""
Apartment API Routes

This module provides REST API endpoints for apartment management including:
- Creating apartments with image uploads
- Retrieving apartment details and listings
- Updating and deleting apartments
- Managing user's own apartments

All apartment modification endpoints (create, update, delete) require authentication.
Ownership validation ensures users can only modify their own apartments.
"""

from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import SessionLocal
from app.services import apartment_service
from app.models.apartment_pyd import ApartmentFilter, ApartmentCreateInput, ApartmentResponse
from app.schemas.user_sql import UserDB
from app.middleware.auth_middleware import get_current_user
from app.utils.apartments_utils import verify_apartment_ownership

router = APIRouter()


# ===========================
# Database Session Management
# ===========================

def get_db():
    """
    Database session dependency.

    Creates a new database session for each request and ensures it's properly
    closed after the request completes.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===========================
# Apartment CRUD Endpoints
# ===========================

@router.post("/apartments", response_model=ApartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_apartment(
    images: List[UploadFile] = File(..., description="At least 4 image files (jpg, png, webp)"),
    title: str = Form(..., description="Apartment title"),
    description: str = Form(..., description="Detailed description"),
    location: str = Form(..., description="Apartment location/address"),
    apartment_type: str = Form(..., description="Type (Studio, 1BHK, 2BHK, etc.)"),
    rent_per_week: int = Form(..., description="Weekly rent amount", gt=0),
    start_date: str = Form(..., description="Availability start date (ISO format)"),
    duration_len: int = Form(None, description="Rental duration in weeks"),
    place_accept: str = Form(..., description="Accepted tenant type (Students, Professionals, Both)"),
    furnishing_type: str = Form(..., description="Furnishing status (Furnished, Semi-Furnished, Unfurnished)"),
    is_pathroom_solo: bool = Form(False, description="Private bathroom (True) or shared (False)"),
    parking_type: str = Form(..., description="Parking availability (Private, Street, Garage, None)"),
    keywords: str = Form(None, description="Comma-separated amenities/keywords"),
    is_active: bool = Form(True, description="Apartment active status"),
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new apartment listing.

    Requires authentication. The apartment is automatically assigned to the current user.
    Uploads and validates at least 4 images. Images must be in JPG, PNG, or WebP format.

    Args:
        images: Minimum 4 image files
        title: Apartment title
        description: Detailed description
        location: Location/address
        apartment_type: Type (Studio, 1BHK, etc.)
        rent_per_week: Weekly rent in currency units
        start_date: ISO format date string
        duration_len: Rental duration in weeks (optional)
        place_accept: Accepted tenant type
        furnishing_type: Furnishing status
        is_pathroom_solo: Private or shared bathroom
        parking_type: Parking availability
        keywords: Comma-separated amenities
        is_active: Active status (default: True)
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        ApartmentResponse: Created apartment details

    Raises:
        HTTPException 400: Invalid data or image validation failed
        HTTPException 401: Authentication required
    """
    apartment_input = ApartmentCreateInput(
        title=title,
        description=description,
        location=location,
        apartment_type=apartment_type,
        rent_per_week=rent_per_week,
        start_date=start_date,
        duration_len=duration_len,
        place_accept=place_accept,
        furnishing_type=furnishing_type,
        is_pathroom_solo=is_pathroom_solo,
        parking_type=parking_type,
        keywords=keywords,
        is_active=is_active,
        renter_id=current_user.id
    )

    return await apartment_service.create_apartment(
        db=db,
        apartment_input=apartment_input,
        images=images
    )


@router.get("/apartments/{apartment_id}", response_model=ApartmentResponse)
def get_apartment_by_id(
    apartment_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific apartment by ID.

    Public endpoint - no authentication required.

    Args:
        apartment_id: Unique apartment identifier
        db: Database session (injected)

    Returns:
        ApartmentResponse: Apartment details

    Raises:
        HTTPException 404: Apartment not found
    """
    apartment = apartment_service.get_apartment_by_id(db, apartment_id)

    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apartment with ID {apartment_id} not found"
        )

    return apartment


@router.get("/apartments", response_model=dict)
def list_apartments(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List all apartments with pagination.

    Public endpoint - no authentication required.
    Returns published and active apartments only.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 10)
        db: Database session (injected)

    Returns:
        dict: Contains 'apartments' list, 'total', 'skip', and 'limit'

    Example:
        GET /apartments?skip=0&limit=20
    """
    apartments = apartment_service.list_apartments(db, skip, limit)
    total = len(apartments)  # TODO: Add proper count query

    return {
        "apartments": apartments,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.put("/apartments/{apartment_id}", response_model=ApartmentResponse)
def update_apartment(
    apartment_id: int,
    apartment_update: ApartmentFilter,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing apartment.

    Requires authentication. Users can only update their own apartments.
    Supports partial updates - only provided fields will be updated.

    Args:
        apartment_id: Apartment to update
        apartment_update: Fields to update (partial update supported)
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        ApartmentResponse: Updated apartment details

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Not the apartment owner
        HTTPException 404: Apartment not found
    """
    apartment = apartment_service.get_apartment_by_id(db, apartment_id)

    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apartment with ID {apartment_id} not found"
        )

    # Verify ownership before update
    verify_apartment_ownership(apartment, current_user.id)

    # Perform update
    updated_apartment = apartment_service.update_apartment(
        db,
        apartment_id,
        apartment_update
    )

    return updated_apartment


@router.delete("/apartments/{apartment_id}", status_code=status.HTTP_200_OK)
def delete_apartment(
    apartment_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an apartment listing.

    Requires authentication. Users can only delete their own apartments.
    Also deletes all associated images from the filesystem.

    Args:
        apartment_id: Apartment to delete
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        dict: Success message

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Not the apartment owner
        HTTPException 404: Apartment not found
    """
    apartment = apartment_service.get_apartment_by_id(db, apartment_id)

    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apartment with ID {apartment_id} not found"
        )

    # Verify ownership before deletion
    verify_apartment_ownership(apartment, current_user.id)

    # Perform deletion
    result = apartment_service.delete_apartment(db, apartment_id)

    return result


# ===========================
# User-Specific Endpoints
# ===========================

@router.get("/my-apartments", response_model=dict)
async def get_my_apartments(
    skip: int = 0,
    limit: int = 100,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all apartments created by the authenticated user.

    Requires authentication. Returns apartments owned by the current user,
    ordered by creation date (newest first). Includes all statuses (draft,
    published, archived).

    Args:
        skip: Number of records to skip for pagination (default: 0)
        limit: Maximum number of records to return (default: 100)
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        dict: Contains 'apartments' list, 'total' count, 'skip', and 'limit'

    Raises:
        HTTPException 401: Authentication required

    Example:
        GET /my-apartments?skip=0&limit=20
    """
    apartments = apartment_service.get_my_apartments(
        db=db,
        renter_id=current_user.id,
        skip=skip,
        limit=limit
    )

    total = apartment_service.get_my_apartments_count(
        db=db,
        renter_id=current_user.id
    )

    return {
        "apartments": [ApartmentResponse.model_validate(apt) for apt in apartments],
        "total": total,
        "skip": skip,
        "limit": limit
    }
