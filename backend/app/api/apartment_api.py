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
from typing import List, Optional

from app.database.database import SessionLocal
from app.services import apartment_service
from app.models.apartment_pyd import ApartmentFilter, ApartmentCreateInput, ApartmentResponse, ApartmentStatus, FeaturedRequest, BulkOperationRequest, BulkOperationResponse, BulkAction
from app.schemas.user_sql import UserDB, UserType
from app.middleware.auth_middleware import get_current_user
from app.utils.apartments_utils import verify_apartment_ownership
from app.schemas.apartment_sql import ApartmentDB
from app.utils.rbac import require_renter

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
    current_user: UserDB = Depends(require_renter),
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
    track_view: bool = True,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific apartment by ID and increment view count.

    Public endpoint - no authentication required.
    Set track_view=false to get details without incrementing counter.

    Args:
        apartment_id: Unique apartment identifier
        track_view: Whether to track this view (default: True)
        db: Database session (injected)

    Returns:
        ApartmentResponse: Apartment details

    Raises:
        HTTPException 404: Apartment not found
    """
    if track_view:
        apartment = apartment_service.increment_view_count(db, apartment_id)
    else:
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
    show_featured_first: bool = True,
    db: Session = Depends(get_db)
):
    """
    List all apartments with pagination.
    Featured apartments appear first by default.

    Public endpoint - no authentication required.
    Returns published and active apartments only.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 10)
        show_featured_first: Show featured apartments first (default: True)
        db: Database session (injected)

    Returns:
        dict: Contains 'apartments' list, 'total', 'skip', and 'limit'

    Example:
        GET /apartments?skip=0&limit=20&show_featured_first=true
    """
    query = db.query(ApartmentDB)\
        .filter(ApartmentDB.status == ApartmentStatus.PUBLISHED)\
        .filter(ApartmentDB.is_active == True)

    if show_featured_first:
        # Order by featured status, then priority, then created date
        query = query.order_by(
            ApartmentDB.is_featured.desc(),
            ApartmentDB.featured_priority.desc(),
            ApartmentDB.created_at.desc()
        )
    else:
        query = query.order_by(ApartmentDB.created_at.desc())

    apartments = query.offset(skip).limit(limit).all()
    total = query.count()

    return {
        "apartments": [ApartmentResponse.model_validate(apt) for apt in apartments],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/apartments/popular/list", response_model=List[ApartmentResponse])
def get_popular_apartments(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get most popular (most viewed) apartments.

    Public endpoint - no authentication required.
    Returns published and active apartments ordered by view count.

    Args:
        limit: Maximum number of apartments to return (default: 10)
        db: Database session (injected)

    Returns:
        List[ApartmentResponse]: List of most viewed apartments

    Example:
        GET /apartments/popular/list?limit=5
    """
    apartments = apartment_service.get_popular_apartments(db, limit)
    return [ApartmentResponse.model_validate(apt) for apt in apartments]


@router.put("/apartments/{apartment_id}", response_model=ApartmentResponse)
def update_apartment(
    apartment_id: int,
    apartment_update: ApartmentFilter,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing apartment.

    Requires authentication.
    - Renters can only update their own apartments
    - Admins can update any apartment

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
        HTTPException 403: Not the apartment owner (for renters)
        HTTPException 404: Apartment not found
    """
    apartment = apartment_service.get_apartment_by_id(db, apartment_id)

    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apartment with ID {apartment_id} not found"
        )

    # Verify ownership before update (unless admin)
    if current_user.role != UserType.ADMIN:
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

    Requires authentication.
    - Renters can only delete their own apartments
    - Admins can delete any apartment

    Also deletes all associated images from the filesystem.

    Args:
        apartment_id: Apartment to delete
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        dict: Success message

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Not the apartment owner (for renters)
        HTTPException 404: Apartment not found
    """
    apartment = apartment_service.get_apartment_by_id(db, apartment_id)

    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Apartment with ID {apartment_id} not found"
        )

    # Verify ownership before deletion (unless admin)
    if current_user.role != UserType.ADMIN:
        verify_apartment_ownership(apartment, current_user.id)

    # Perform deletion
    result = apartment_service.delete_apartment(db, apartment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Apartment deletion failed")

    return result


# ===========================
# User-Specific Endpoints
# ===========================

@router.post("/{apartment_id}/publish", response_model=ApartmentResponse)
async def publish_apartment(
    apartment_id: int,
    current_user: UserDB = Depends(require_renter),
    db: Session = Depends(get_db)
):
    """Publish a draft apartment."""
    apartment = apartment_service.get_apartment_by_id(db, apartment_id)
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")

    verify_apartment_ownership(apartment, current_user.id)

    if apartment.status == ApartmentStatus.PUBLISHED:
        raise HTTPException(status_code=400, detail="Apartment is already published")

    updated = apartment_service.publish_apartment(db, apartment_id)
    return ApartmentResponse.model_validate(updated)


@router.post("/{apartment_id}/archive", response_model=ApartmentResponse)
async def archive_apartment(
    apartment_id: int,
    current_user: UserDB = Depends(require_renter),
    db: Session = Depends(get_db)
):
    """Archive a published apartment."""
    apartment = apartment_service.get_apartment_by_id(db, apartment_id)
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")

    verify_apartment_ownership(apartment, current_user.id)

    updated = apartment_service.archive_apartment(db, apartment_id)
    return ApartmentResponse.model_validate(updated)


@router.get("/my-apartments", response_model=dict)
async def get_my_apartments(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ApartmentStatus] = None,
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

    query = db.query(ApartmentDB).filter(ApartmentDB.renter_id == current_user.id)
    
    if status:
        query = query.filter(ApartmentDB.status == status)
        
    apartments = query.order_by(ApartmentDB.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

    total = query.count()

    return {
        "apartments": [ApartmentResponse.model_validate(apt) for apt in apartments],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/my-apartments/analytics", response_model=dict)
async def get_my_apartments_analytics(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get analytics for user's apartments.

    Requires authentication. Returns view statistics for all apartments
    owned by the current user.

    Args:
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        dict: Contains total_apartments, total_views, average_views_per_apartment,
              and most_viewed_apartment

    Raises:
        HTTPException 401: Authentication required

    Example:
        GET /my-apartments/analytics
    """
    apartments = db.query(ApartmentDB)\
        .filter(ApartmentDB.renter_id == current_user.id)\
        .all()

    total_views = sum(apt.view_count for apt in apartments)
    avg_views = total_views / len(apartments) if apartments else 0

    most_viewed = max(apartments, key=lambda x: x.view_count) if apartments else None

    return {
        "total_apartments": len(apartments),
        "total_views": total_views,
        "average_views_per_apartment": round(avg_views, 2),
        "most_viewed_apartment": ApartmentResponse.model_validate(most_viewed) if most_viewed else None
    }


@router.post("/{apartment_id}/feature", response_model=ApartmentResponse)
async def feature_apartment_endpoint(
    apartment_id: int,
    featured_request: FeaturedRequest,
    current_user: UserDB = Depends(require_renter),
    db: Session = Depends(get_db)
):
    """
    Feature an apartment (owner or admin only).
    Featured apartments appear at the top of search results.

    Args:
        apartment_id: ID of apartment to feature
        featured_request: Feature request with duration and priority
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        ApartmentResponse: Updated apartment with featured status

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Not the apartment owner
        HTTPException 404: Apartment not found
    """
    apartment = apartment_service.get_apartment_by_id(db, apartment_id)
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")

    verify_apartment_ownership(apartment, current_user.id)

    # In production, you might want to check payment here
    # or restrict this to admin users only

    updated = apartment_service.feature_apartment(
        db,
        apartment_id,
        featured_request.duration_days,
        featured_request.priority
    )

    return ApartmentResponse.model_validate(updated)


@router.delete("/{apartment_id}/feature", response_model=ApartmentResponse)
async def unfeature_apartment_endpoint(
    apartment_id: int,
    current_user: UserDB = Depends(require_renter),
    db: Session = Depends(get_db)
):
    """
    Remove featured status from apartment.

    Args:
        apartment_id: ID of apartment to unfeature
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        ApartmentResponse: Updated apartment without featured status

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Not the apartment owner
        HTTPException 404: Apartment not found
    """
    apartment = apartment_service.get_apartment_by_id(db, apartment_id)
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")

    verify_apartment_ownership(apartment, current_user.id)

    updated = apartment_service.unfeature_apartment(db, apartment_id)
    return ApartmentResponse.model_validate(updated)


@router.get("/featured/list", response_model=List[ApartmentResponse])
async def get_featured_apartments_endpoint(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get currently featured apartments.

    Public endpoint - no authentication required.
    Returns featured apartments that haven't expired, ordered by priority.

    Args:
        limit: Maximum number of apartments to return (default: 10)
        db: Database session (injected)

    Returns:
        List[ApartmentResponse]: List of featured apartments

    Example:
        GET /featured/list?limit=5
    """
    apartments = apartment_service.get_featured_apartments(db, limit)
    return [ApartmentResponse.model_validate(apt) for apt in apartments]


@router.post("/{apartment_id}/duplicate", response_model=ApartmentResponse)
async def duplicate_apartment_endpoint(
    apartment_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a duplicate copy of an apartment.
    User must own the original apartment to duplicate it.
    The duplicate is created as a DRAFT.

    Args:
        apartment_id: ID of apartment to duplicate
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        ApartmentResponse: The duplicated apartment

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Not the apartment owner
        HTTPException 404: Apartment not found
        HTTPException 500: Duplication failed
    """
    original = apartment_service.get_apartment_by_id(db, apartment_id)
    if not original:
        raise HTTPException(status_code=404, detail="Apartment not found")

    # Verify ownership
    verify_apartment_ownership(original, current_user.id)

    # Create duplicate
    duplicate = apartment_service.duplicate_apartment(db, apartment_id, current_user.id)

    if not duplicate:
        raise HTTPException(status_code=500, detail="Failed to duplicate apartment")

    return ApartmentResponse.model_validate(duplicate)


@router.post("/bulk-operation", response_model=BulkOperationResponse)
async def bulk_apartment_operation(
    bulk_request: BulkOperationRequest,
    current_user: UserDB = Depends(require_renter),
    db: Session = Depends(get_db)
):
    """
    Perform bulk operations on multiple apartments.
    User can only perform operations on their own apartments.

    Actions:
    - PUBLISH: Change status to published
    - ARCHIVE: Change status to archived
    - DELETE: Permanently delete apartments
    - ACTIVATE: Set is_active to true
    - DEACTIVATE: Set is_active to false
    - FEATURE: Mark as featured
    - UNFEATURE: Remove featured status

    Args:
        bulk_request: Bulk operation request
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        BulkOperationResponse: Operation results

    Raises:
        HTTPException 401: Authentication required
    """
    # Build kwargs for action-specific parameters
    kwargs = {}
    if bulk_request.action == BulkAction.FEATURE:
        kwargs['featured_duration_days'] = bulk_request.featured_duration_days or 30
        kwargs['featured_priority'] = bulk_request.featured_priority or 5

    # Perform bulk operation
    results = apartment_service.bulk_operation(
        db=db,
        apartment_ids=bulk_request.apartment_ids,
        action=bulk_request.action.value,
        user_id=current_user.id,
        **kwargs
    )

    return BulkOperationResponse(**results)


@router.get("/my-apartments/ids", response_model=dict)
async def get_my_apartment_ids(
    status: Optional[ApartmentStatus] = None,
    is_active: Optional[bool] = None,
    is_featured: Optional[bool] = None,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of apartment IDs matching criteria.
    Useful for bulk operations (e.g., 'select all drafts').

    Args:
        status: Filter by status (optional)
        is_active: Filter by active status (optional)
        is_featured: Filter by featured status (optional)
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        dict: Contains apartment_ids list and count

    Raises:
        HTTPException 401: Authentication required

    Example:
        GET /my-apartments/ids?status=DRAFT&is_active=true
    """
    query = db.query(ApartmentDB.id)\
        .filter(ApartmentDB.renter_id == current_user.id)

    if status:
        query = query.filter(ApartmentDB.status == status)
    if is_active is not None:
        query = query.filter(ApartmentDB.is_active == is_active)
    if is_featured is not None:
        query = query.filter(ApartmentDB.is_featured == is_featured)

    ids = [row[0] for row in query.all()]

    return {
        "apartment_ids": ids,
        "count": len(ids)
    }
