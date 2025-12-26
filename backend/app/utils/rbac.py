from functools import wraps
from fastapi import HTTPException, status, Depends
from app.schemas.user_sql import UserDB, UserType
from app.middleware.auth_middleware import get_current_user

def require_role(*allowed_roles: UserType):
    """
    Decorator to enforce role-based access control.

    Usage:
        @require_role(UserType.RENTER)
        async def create_apartment(...):
            ...

    Args:
        allowed_roles: One or more UserType values

    Raises:
        HTTPException 403: If user doesn't have required role
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            # Check if user has required role
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"This action requires one of the following roles: {[r.value for r in allowed_roles]}"
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_renter(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    """
    Dependency to ensure user is a RENTER.

    Usage:
        @router.post("/apartments")
        async def create_apartment(
            current_user: UserDB = Depends(require_renter),
            db: Session = Depends(get_db)
        ):
            ...
    """
    if current_user.role != UserType.RENTER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only renters can perform this action"
        )
    return current_user


def require_renter_or_admin(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    """
    Dependency to ensure user is a RENTER or ADMIN.
    Admins have full access to all renter operations.

    Usage:
        @router.post("/apartments")
        async def create_apartment(
            current_user: UserDB = Depends(require_renter_or_admin),
            db: Session = Depends(get_db)
        ):
            ...
    """
    if current_user.role not in (UserType.RENTER, UserType.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only renters or admins can perform this action"
        )
    return current_user


def require_admin(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    """
    Dependency to ensure user is an ADMIN.

    Usage:
        @router.delete("/users/{user_id}")
        async def delete_user(
            user_id: int,
            current_user: UserDB = Depends(require_admin),
            db: Session = Depends(get_db)
        ):
            ...
    """
    if current_user.role != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user