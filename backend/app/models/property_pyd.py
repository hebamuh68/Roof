from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

from app.schemas.enums import FacilityType, ConstraintType, PropertyStatus


class SortOption(str, Enum):
    RELEVANCE = "relevance"
    PRICE_LOW_HIGH = "price_asc"
    PRICE_HIGH_LOW = "price_desc"
    DATE_NEWEST = "date_desc"
    DATE_OLDEST = "date_asc"


class PropertyCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    type: str = Field(..., description="Type (Studio, 1BHK, 2BHK, etc.)")
    street: Optional[str] = None
    zone: Optional[str] = None
    government: Optional[str] = None
    rent: int = Field(..., gt=0)
    availability_start: Optional[datetime] = None
    availability_duration: Optional[int] = Field(None, ge=1)
    facilities: Optional[List[FacilityType]] = None
    constraints: Optional[List[ConstraintType]] = None
    status: Optional[PropertyStatus] = PropertyStatus.DRAFT

    model_config = ConfigDict(from_attributes=True)


class PropertyResponse(BaseModel):
    property_id: int
    user_id: str
    title: str
    description: Optional[str] = None
    type: str
    status: PropertyStatus
    street: Optional[str] = None
    zone: Optional[str] = None
    government: Optional[str] = None
    rent: int
    availability_start: Optional[datetime] = None
    availability_duration: Optional[int] = None
    facilities: Optional[List[FacilityType]] = None
    constraints: Optional[List[ConstraintType]] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PropertyFilter(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    type: Optional[str] = None
    street: Optional[str] = None
    zone: Optional[str] = None
    government: Optional[str] = None
    rent: Optional[int] = Field(None, gt=0)
    availability_start: Optional[datetime] = None
    availability_duration: Optional[int] = Field(None, ge=1)
    facilities: Optional[List[FacilityType]] = None
    constraints: Optional[List[ConstraintType]] = None
    status: Optional[PropertyStatus] = None

    model_config = ConfigDict(from_attributes=True)
