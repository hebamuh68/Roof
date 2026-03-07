from fastapi import HTTPException, status, Depends
from app.schemas.user_sql import UserDB
from app.middleware.auth_middleware import get_current_user


def require_admin(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
