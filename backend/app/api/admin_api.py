from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.user_sql import UserDB
from app.middleware.auth_middleware import get_current_user
from app.services import user_service

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/users", response_model=List[dict])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return user_service.list_all_users(db, skip=skip, limit=limit)


@router.delete("/users/{user_email}")
async def delete_user(
    user_email: str,
    current_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = user_service.get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_email} not found")

    result = user_service.delete_user(db, user_email)
    if not result:
        raise HTTPException(status_code=304, detail="User deletion failed")

    return result


@router.get("/stats")
async def get_platform_stats(
    current_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db),
):
    from sqlalchemy import func
    from app.schemas.property_sql import PropertyDB
    from app.schemas.enums import PropertyStatus

    total_users = db.query(func.count(UserDB.email)).scalar()
    total_properties = db.query(func.count(PropertyDB.property_id)).scalar()

    draft_count = db.query(func.count(PropertyDB.property_id))\
        .filter(PropertyDB.status == PropertyStatus.DRAFT).scalar()
    published_count = db.query(func.count(PropertyDB.property_id))\
        .filter(PropertyDB.status == PropertyStatus.PUBLISHED).scalar()
    archived_count = db.query(func.count(PropertyDB.property_id))\
        .filter(PropertyDB.status == PropertyStatus.ARCHIVED).scalar()

    return {
        "total_users": total_users,
        "total_properties": total_properties,
        "properties_by_status": {
            "draft": draft_count,
            "published": published_count,
            "archived": archived_count,
        },
    }
