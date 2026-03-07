from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.services import property_service
from app.models.property_pyd import PropertyCreate, PropertyResponse, PropertyFilter
from app.schemas.property_sql import PropertyDB
from app.schemas.enums import PropertyStatus
from app.schemas.user_sql import UserDB
from app.middleware.auth_middleware import get_current_user

router = APIRouter()


@router.post("/properties", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_data: PropertyCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = await property_service.create_property(db, property_data, current_user.email)
    return PropertyResponse.model_validate(result)


@router.get("/properties", response_model=dict)
def list_properties(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    properties = property_service.list_properties(db, skip, limit)
    total = len(properties)
    return {
        "properties": [PropertyResponse.model_validate(p) for p in properties],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/properties/{property_id}", response_model=PropertyResponse)
def get_property_by_id(
    property_id: int,
    db: Session = Depends(get_db),
):
    prop = property_service.get_property_by_id(db, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail=f"Property with ID {property_id} not found")
    return PropertyResponse.model_validate(prop)


@router.put("/properties/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: int,
    property_update: PropertyFilter,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prop = property_service.get_property_by_id(db, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail=f"Property with ID {property_id} not found")

    if prop.user_id != current_user.email and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have permission to modify this property")

    updated = property_service.update_property(db, property_id, property_update)
    return PropertyResponse.model_validate(updated)


@router.delete("/properties/{property_id}")
def delete_property(
    property_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prop = property_service.get_property_by_id(db, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail=f"Property with ID {property_id} not found")

    if prop.user_id != current_user.email and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this property")

    result = property_service.delete_property(db, property_id)
    if not result:
        raise HTTPException(status_code=404, detail="Property deletion failed")
    return result


@router.post("/properties/{property_id}/publish", response_model=PropertyResponse)
async def publish_property(
    property_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prop = property_service.get_property_by_id(db, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    if prop.user_id != current_user.email and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    if prop.status == PropertyStatus.PUBLISHED:
        raise HTTPException(status_code=400, detail="Property is already published")

    updated = property_service.publish_property(db, property_id)
    return PropertyResponse.model_validate(updated)


@router.post("/properties/{property_id}/archive", response_model=PropertyResponse)
async def archive_property(
    property_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prop = property_service.get_property_by_id(db, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    if prop.user_id != current_user.email and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    updated = property_service.archive_property(db, property_id)
    return PropertyResponse.model_validate(updated)


@router.get("/my-properties", response_model=dict)
async def get_my_properties(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[PropertyStatus] = Query(None, alias="status"),
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    properties = property_service.get_user_properties(
        db, current_user.email, skip, limit, status_filter
    )
    return {
        "properties": [PropertyResponse.model_validate(p) for p in properties],
        "total": len(properties),
        "skip": skip,
        "limit": limit,
    }
