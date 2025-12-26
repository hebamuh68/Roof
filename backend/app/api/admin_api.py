from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.user_sql import UserDB
from app.utils.rbac import require_admin
from app.services import user_service, apartment_service
from app.schemas.user_sql import UserDB, UserType

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

@router.get("/users", response_model=List[dict])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Retrieve all users in the system. Admin access required.
    """
    if current_user.role != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="You don't have permission for this action")

    users = user_service.list_all_users(db, skip=skip, limit=limit)
    return users


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Delete a user. Admin access required.
    """

    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    if current_user.role != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="You don't have permission for this action")

    result = user_service.delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=304, detail="User deletion failed")
    
    return result


@router.get("/stats")
async def get_platform_stats(
    current_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get platform statistics (admin only)."""
    from sqlalchemy import func
    from app.schemas.apartment_sql import ApartmentDB, ApartmentStatus

    if current_user.role != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="You don't have permission for this action")

    total_users = db.query(func.count(UserDB.id)).scalar()
    total_apartments = db.query(func.count(ApartmentDB.id)).scalar()
    active_apartments = db.query(func.count(ApartmentDB.id))\
        .filter(ApartmentDB.is_active == True).scalar()

    seekers_count = db.query(func.count(UserDB.id))\
        .filter(UserDB.role == UserType.SEEKER).scalar()
    renters_count = db.query(func.count(UserDB.id))\
        .filter(UserDB.role == UserType.RENTER).scalar()
    admins_count = db.query(func.count(UserDB.id))\
        .filter(UserDB.role == UserType.ADMIN).scalar()

    # Get apartment counts by status
    draft_count = db.query(func.count(ApartmentDB.id))\
        .filter(ApartmentDB.status == ApartmentStatus.DRAFT).scalar()
    published_count = db.query(func.count(ApartmentDB.id))\
        .filter(ApartmentDB.status == ApartmentStatus.PUBLISHED).scalar()
    archived_count = db.query(func.count(ApartmentDB.id))\
        .filter(ApartmentDB.status == ApartmentStatus.ARCHIVED).scalar()

    return {
        "total_users": total_users,
        "total_apartments": total_apartments,
        "active_apartments": active_apartments,
        "seekers": seekers_count,
        "renters": renters_count,
        "users_by_role": {
            "seeker": seekers_count,
            "renter": renters_count,
            "admin": admins_count
        },
        "apartments_by_status": {
            "draft": draft_count,
            "published": published_count,
            "archived": archived_count
        }
    }