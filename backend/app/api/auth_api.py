from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.models.auth_pyd import Token, RefreshTokenRequest
from app.models.user_pyd import UserCreate, UserLogin, UserResponse
from app.schemas.user_sql import UserDB
from app.database.database import get_db
from app.services.auth_service import create_user, login_user, get_user, refresh_access_token
from app.middleware.auth_middleware import get_current_user
from app.utils.auth import get_password_hash
from app.utils.validators import get_password_strength_score

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.post("/auth/register", response_model=dict)
@limiter.limit("5/hour")
async def register(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(user_data, db)


@router.post("/auth/login", response_model=Token)
@limiter.limit("10/minute")
async def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    return login_user(credentials, db)


@router.post("/auth/refresh", response_model=Token)
@limiter.limit("20/minute")
async def refresh_token(
    request: Request,
    token_request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    return refresh_access_token(token_request.refresh_token, db)


@router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: UserDB = Depends(get_current_user)):
    return get_user(current_user)


class PasswordStrengthRequest(BaseModel):
    password: str


@router.post("/auth/check-password-strength")
async def check_password_strength(password_request: PasswordStrengthRequest):
    return get_password_strength_score(password_request.password)


@router.get("/auth/profile-completeness")
async def get_profile_completeness(current_user: UserDB = Depends(get_current_user)):
    user_dict = {
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "phone": current_user.phone,
        "gender": current_user.gender,
        "job_title": current_user.job_title,
    }

    filled = sum(1 for v in user_dict.values() if v)
    total = len(user_dict)
    percentage = int((filled / total) * 100)

    missing = [k for k, v in user_dict.items() if not v]

    return {
        "completion_percentage": percentage,
        "missing_fields": missing,
        "is_complete": len(missing) == 0,
    }
