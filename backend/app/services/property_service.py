from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from typing import List, Optional
from pathlib import Path
from datetime import datetime, timezone

from app.schemas.property_sql import PropertyDB
from app.schemas.property_image_sql import PropertyImageDB
from app.schemas.enums import PropertyStatus
from app.models.property_pyd import PropertyCreate, PropertyFilter
from app.utils.image_upload import save_multiple_images, get_image_url, delete_image_file


async def create_property(
    db: Session,
    property_data: PropertyCreate,
    user_email: str,
    images: Optional[List[UploadFile]] = None,
) -> PropertyDB:
    db_property = PropertyDB(
        user_id=user_email,
        title=property_data.title,
        description=property_data.description,
        type=property_data.type,
        street=property_data.street,
        zone=property_data.zone,
        government=property_data.government,
        rent=property_data.rent,
        availability_start=property_data.availability_start,
        availability_duration=property_data.availability_duration,
        facilities=[f.value for f in property_data.facilities] if property_data.facilities else None,
        constraints=[c.value for c in property_data.constraints] if property_data.constraints else None,
        status=property_data.status or PropertyStatus.DRAFT,
    )

    db.add(db_property)
    db.commit()
    db.refresh(db_property)

    if images:
        saved_filenames = await save_multiple_images(images)
        for filename in saved_filenames:
            image_url = get_image_url(filename)
            db_image = PropertyImageDB(
                image_url=image_url,
                property_id=db_property.property_id,
            )
            db.add(db_image)
        db.commit()
        db.refresh(db_property)

    return db_property


def get_property_by_id(db: Session, property_id: int) -> Optional[PropertyDB]:
    return db.query(PropertyDB).filter(PropertyDB.property_id == property_id).first()


def get_user_properties(
    db: Session,
    user_email: str,
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[PropertyStatus] = None,
) -> List[PropertyDB]:
    query = db.query(PropertyDB).filter(PropertyDB.user_id == user_email)

    if status_filter:
        query = query.filter(PropertyDB.status == status_filter)

    return query.order_by(PropertyDB.created_at.desc()).offset(skip).limit(limit).all()


def list_properties(
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> List[PropertyDB]:
    return db.query(PropertyDB)\
        .filter(PropertyDB.status == PropertyStatus.PUBLISHED)\
        .order_by(PropertyDB.created_at.desc())\
        .offset(skip).limit(limit).all()


def update_property(
    db: Session,
    property_id: int,
    property_data: PropertyFilter,
) -> Optional[PropertyDB]:
    db_property = db.query(PropertyDB).filter(PropertyDB.property_id == property_id).first()
    if not db_property:
        return None

    update_data = property_data.model_dump(exclude_unset=True)

    if "facilities" in update_data and update_data["facilities"] is not None:
        update_data["facilities"] = [f.value for f in update_data["facilities"]]
    if "constraints" in update_data and update_data["constraints"] is not None:
        update_data["constraints"] = [c.value for c in update_data["constraints"]]

    for field, value in update_data.items():
        setattr(db_property, field, value)

    db.commit()
    db.refresh(db_property)
    return db_property


def publish_property(db: Session, property_id: int) -> Optional[PropertyDB]:
    prop = get_property_by_id(db, property_id)
    if not prop:
        return None
    prop.status = PropertyStatus.PUBLISHED
    db.commit()
    db.refresh(prop)
    return prop


def archive_property(db: Session, property_id: int) -> Optional[PropertyDB]:
    prop = get_property_by_id(db, property_id)
    if not prop:
        return None
    prop.status = PropertyStatus.ARCHIVED
    db.commit()
    db.refresh(prop)
    return prop


def delete_property(db: Session, property_id: int) -> Optional[dict]:
    db_property = db.query(PropertyDB).filter(PropertyDB.property_id == property_id).first()
    if not db_property:
        return None

    if db_property.images:
        for img in db_property.images:
            filename = Path(img.image_url).name
            delete_image_file(filename)

    db.delete(db_property)
    db.commit()

    return {"message": "Property deleted successfully"}
