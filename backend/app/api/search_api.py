from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models.property_pyd import PropertyFilter, PropertyResponse, SortOption
from app.schemas.property_sql import PropertyDB
from app.schemas.enums import PropertyStatus
from app.database.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/search/properties")
def search(
    query: str = Query(..., min_length=1, description="Search query string"),
    sort_by: SortOption = Query(SortOption.RELEVANCE, description="Sort order"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    search_term = f"%{query.lower()}%"

    search_conditions = or_(
        func.lower(PropertyDB.title).like(search_term),
        func.lower(PropertyDB.description).like(search_term),
        func.lower(PropertyDB.zone).like(search_term),
        func.lower(PropertyDB.government).like(search_term),
        func.lower(PropertyDB.type).like(search_term),
    )

    base_query = db.query(PropertyDB).filter(
        search_conditions,
        PropertyDB.status == PropertyStatus.PUBLISHED,
    )

    if sort_by == SortOption.PRICE_LOW_HIGH:
        base_query = base_query.order_by(PropertyDB.rent.asc())
    elif sort_by == SortOption.PRICE_HIGH_LOW:
        base_query = base_query.order_by(PropertyDB.rent.desc())
    elif sort_by == SortOption.DATE_NEWEST:
        base_query = base_query.order_by(PropertyDB.created_at.desc())
    elif sort_by == SortOption.DATE_OLDEST:
        base_query = base_query.order_by(PropertyDB.created_at.asc())
    else:
        base_query = base_query.order_by(PropertyDB.created_at.desc())

    properties = base_query.offset(skip).limit(limit).all()
    return [PropertyResponse.model_validate(p) for p in properties]


@router.post("/filter/properties")
def filter_properties(
    filters: PropertyFilter,
    sort_by: SortOption = Query(SortOption.DATE_NEWEST),
    db: Session = Depends(get_db),
):
    query = db.query(PropertyDB).filter(PropertyDB.status == PropertyStatus.PUBLISHED)

    if filters.title:
        query = query.filter(func.lower(PropertyDB.title).like(f"%{filters.title.lower()}%"))
    if filters.type:
        query = query.filter(PropertyDB.type == filters.type)
    if filters.zone:
        query = query.filter(func.lower(PropertyDB.zone).like(f"%{filters.zone.lower()}%"))
    if filters.government:
        query = query.filter(func.lower(PropertyDB.government).like(f"%{filters.government.lower()}%"))
    if filters.rent:
        query = query.filter(PropertyDB.rent <= filters.rent)
    if filters.availability_start:
        query = query.filter(PropertyDB.availability_start >= filters.availability_start)
    if filters.availability_duration:
        query = query.filter(PropertyDB.availability_duration >= filters.availability_duration)

    if sort_by == SortOption.PRICE_LOW_HIGH:
        query = query.order_by(PropertyDB.rent.asc())
    elif sort_by == SortOption.PRICE_HIGH_LOW:
        query = query.order_by(PropertyDB.rent.desc())
    elif sort_by == SortOption.DATE_OLDEST:
        query = query.order_by(PropertyDB.created_at.asc())
    else:
        query = query.order_by(PropertyDB.created_at.desc())

    properties = query.all()
    return [PropertyResponse.model_validate(p) for p in properties]


@router.get("/autocomplete")
def autocomplete(
    query: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    search_term = f"%{query}%"

    titles = db.query(PropertyDB.title).filter(
        PropertyDB.title.ilike(search_term),
        PropertyDB.status == PropertyStatus.PUBLISHED,
    ).distinct().limit(limit).all()

    zones = db.query(PropertyDB.zone).filter(
        PropertyDB.zone.ilike(search_term),
        PropertyDB.status == PropertyStatus.PUBLISHED,
    ).distinct().limit(limit).all()

    return {
        "titles": [t[0] for t in titles],
        "zones": [z[0] for z in zones if z[0]],
    }
