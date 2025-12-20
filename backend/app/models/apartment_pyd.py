"""
Apartment Pydantic Models

This module defines Pydantic models for apartment data validation and serialization.
These models are used throughout the application for:
- Request validation (API input)
- Response serialization (API output)
- Data transformation between layers
- Type safety and IDE support

Models:
    ApartmentCreateInput: Input data from API for creating apartments
    ApartmentRequest: Validated apartment data for service layer
    ApartmentResponse: Apartment data for API responses
    ApartmentFilter: Partial update and filtering model
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

class SortOption(str, Enum):
    """Available sort options for apartment search"""
    RELEVANCE = "relevance"
    PRICE_LOW_HIGH = "price_asc" 
    PRICE_HIGH_LOW = "price_desc" 
    DATE_NEWEST = "date_desc" 
    DATE_OLDEST = "date_asc" 
    VIEWS_HIGH_LOW = "views_desc" 
    FEATURED_FIRST = "featured"


class ApartmentStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class ApartmentCreateInput(BaseModel):
    """
    Input model for apartment creation from API form data.

    This model accepts raw form data from the API endpoint and validates it
    before passing to the service layer. Images are handled separately as
    UploadFile objects cannot be validated by Pydantic.

    Attributes:
        title: Apartment title/name
        description: Detailed description of the apartment
        location: Physical address or location
        apartment_type: Type (e.g., Studio, 1BHK, 2BHK, 3BHK)
        rent_per_week: Weekly rental cost
        start_date: Availability start date (ISO format string)
        duration_len: Rental duration in weeks (optional)
        place_accept: Accepted tenant type (Students, Professionals, Both)
        furnishing_type: Furnishing status (Furnished, Semi-Furnished, Unfurnished)
        is_pathroom_solo: True for private bathroom, False for shared
        parking_type: Parking availability (Private, Street, Garage, None)
        keywords: Comma-separated amenities/features string (optional)
        is_active: Whether the listing is active
        renter_id: ID of the user creating the apartment (auto-assigned)

    Note:
        - start_date is a string here, converted to datetime in service layer
        - keywords is a string here, converted to list in service layer
        - Images are validated separately (minimum 4 required)
    """

    title: str = Field(..., min_length=1, max_length=200, description="Apartment title")
    description: str = Field(..., min_length=1, description="Detailed description")
    location: str = Field(..., min_length=1, max_length=300, description="Location/address")
    apartment_type: str = Field(..., description="Type (Studio, 1BHK, 2BHK, etc.)")
    rent_per_week: int = Field(..., gt=0, description="Weekly rent amount")
    start_date: str = Field(..., description="Availability start date (ISO format)")
    duration_len: Optional[int] = Field(None, ge=1, description="Rental duration in weeks")
    place_accept: str = Field(..., description="Accepted tenant type")
    furnishing_type: str = Field(..., description="Furnishing status")
    is_pathroom_solo: bool = Field(False, description="Private bathroom flag")
    parking_type: str = Field(..., description="Parking availability type")
    keywords: Optional[str] = Field(None, description="Comma-separated amenities")
    is_active: bool = Field(True, description="Active listing flag")
    renter_id: int = Field(..., description="Owner user ID")
    status: Optional[ApartmentStatus] = ApartmentStatus.DRAFT

    model_config = ConfigDict(from_attributes=True)


class ApartmentRequest(BaseModel):
    """
    Validated apartment model for service layer operations.

    This model represents fully validated apartment data ready for database
    insertion. All transformations (date parsing, keyword splitting, image
    validation) have been completed.

    Attributes:
        images: List of image URLs/paths (minimum 4 required)
        title: Apartment title
        description: Detailed description
        location: Physical address
        apartment_type: Type classification
        rent_per_week: Weekly rental cost
        start_date: Availability start date (datetime object)
        duration_len: Rental duration in weeks
        place_accept: Accepted tenant type
        furnishing_type: Furnishing status
        is_pathroom_solo: Private bathroom flag
        parking_type: Parking availability
        keywords: List of amenity/feature strings
        is_active: Active listing flag
        renter_id: Owner user ID

    Validation:
        - Minimum 4 images required
        - All required fields must be present
        - Date must be valid datetime object
    """

    images: List[str] = Field(
        ...,
        min_length=4,
        description="Image URLs (minimum 4)"
    )
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1, max_length=300)
    apartment_type: str
    rent_per_week: int = Field(..., gt=0)
    start_date: datetime
    duration_len: Optional[int] = Field(None, ge=1)
    place_accept: str
    furnishing_type: str
    is_pathroom_solo: bool = False
    parking_type: str
    keywords: Optional[List[str]] = None
    is_active: bool = True
    renter_id: Optional[int] = None

    @field_validator('images')
    @classmethod
    def validate_images(cls, v: List[str]) -> List[str]:
        """
        Validate that at least 4 images are provided.

        Args:
            v: List of image URLs/paths

        Returns:
            List[str]: Validated image list

        Raises:
            ValueError: If fewer than 4 images provided
        """
        if len(v) < 4:
            raise ValueError('At least 4 images are required for apartment listing')
        return v

    model_config = ConfigDict(from_attributes=True)


class ApartmentResponse(BaseModel):
    """
    Apartment response model for API output.

    This model is used to serialize apartment data for API responses.
    Contains all apartment information including relationships.

    Attributes:
        id: Unique apartment identifier
        images: List of image URLs
        title: Apartment title
        description: Detailed description
        location: Physical address
        apartment_type: Type classification
        rent_per_week: Weekly rental cost
        start_date: Availability start date
        duration_len: Rental duration in weeks
        place_accept: Accepted tenant type
        furnishing_type: Furnishing status
        is_pathroom_solo: Private bathroom flag
        parking_type: Parking availability
        keywords: List of amenities/features
        is_active: Active listing flag
        renter_id: Owner user ID

    Usage:
        Used in all apartment retrieval endpoints to ensure consistent
        response format. Automatically converts SQLAlchemy models to
        JSON-serializable dictionaries.
    """

    id: int = Field(..., description="Unique apartment ID")
    images: List[str] = Field(..., description="Image URLs")
    title: str = Field(..., description="Apartment title")
    description: str = Field(..., description="Description")
    location: str = Field(..., description="Location/address")
    apartment_type: str = Field(..., description="Type classification")
    rent_per_week: int = Field(..., description="Weekly rent")
    start_date: datetime = Field(..., description="Availability start date")
    duration_len: Optional[int] = Field(None, description="Duration in weeks")
    place_accept: str = Field(..., description="Accepted tenant type")
    furnishing_type: str = Field(..., description="Furnishing status")
    is_pathroom_solo: bool = Field(..., description="Private bathroom")
    parking_type: str = Field(..., description="Parking type")
    keywords: Optional[List[str]] = Field(None, description="Amenities list")
    is_active: bool = Field(..., description="Active status")
    renter_id: Optional[int] = Field(None, description="Owner user ID")
    status: ApartmentStatus
    view_count: int = Field(default=0, description="Number of views")
    last_viewed_at: Optional[datetime] = Field(None, description="Last viewed timestamp")
    is_featured: bool = Field(default=False, description="Featured status")
    featured_until: Optional[datetime] = Field(None, description="Featured expiration")
    featured_priority: int = Field(default=0, description="Featured priority level")


    model_config = ConfigDict(from_attributes=True)


class ApartmentFilter(BaseModel):
    """
    Apartment filter and partial update model.

    This model supports partial updates and filtering operations.
    All fields are optional, allowing clients to update or filter
    by any combination of fields.

    Attributes:
        All apartment fields as optional values

    Usage:
        - Partial updates: Only provided fields will be updated
        - Filtering: Used in search/filter endpoints
        - Flexible queries: Combine multiple filter criteria

    Example:
        # Update only title and rent
        filter = ApartmentFilter(title="New Title", rent_per_week=1500)

        # Filter by location and type
        filter = ApartmentFilter(location="New York", apartment_type="Studio")
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    apartment_type: Optional[str] = None
    rent_per_week: Optional[int] = Field(None, gt=0)
    start_date: Optional[datetime] = None
    duration_len: Optional[int] = Field(None, ge=1)
    place_accept: Optional[str] = None
    furnishing_type: Optional[str] = None
    is_pathroom_solo: Optional[bool] = None
    parking_type: Optional[str] = None
    keywords: Optional[List[str]] = None
    is_active: Optional[bool] = None
    status: Optional[ApartmentStatus] = None

    model_config = ConfigDict(from_attributes=True)


class FeaturedRequest(BaseModel):
    """Request to feature an apartment."""
    duration_days: int = Field(ge=1, le=90, description="Duration in days (1-90)")
    priority: int = Field(ge=1, le=10, default=5, description="Priority level (1-10)")


class BulkAction(str, Enum):
    """Available bulk operation actions."""
    PUBLISH = "PUBLISH"
    ARCHIVE = "ARCHIVE"
    DELETE = "DELETE"
    ACTIVATE = "ACTIVATE"
    DEACTIVATE = "DEACTIVATE"
    FEATURE = "FEATURE"
    UNFEATURE = "UNFEATURE"


class BulkOperationRequest(BaseModel):
    """Request for bulk operations on apartments."""
    apartment_ids: List[int] = Field(..., min_length=1, max_length=100, description="Apartment IDs (max 100)")
    action: BulkAction = Field(..., description="Action to perform")

    # Optional parameters for specific actions
    featured_duration_days: Optional[int] = Field(None, ge=1, le=90, description="Duration for FEATURE action")
    featured_priority: Optional[int] = Field(None, ge=1, le=10, description="Priority for FEATURE action")


class BulkOperationResponse(BaseModel):
    """Response from bulk operations."""
    total_requested: int = Field(..., description="Total apartments requested")
    successful: int = Field(..., description="Successfully processed")
    failed: int = Field(..., description="Failed to process")
    errors: List[dict] = Field(default_factory=list, description="Error details")
    updated_apartments: List[int] = Field(default_factory=list, description="IDs of updated apartments")
