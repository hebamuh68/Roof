from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.auth_pyd import Token
from app.models.user_pyd import UserData, UserLogin
from app.schemas.user_sql import UserDB as User
from app.database.database import get_db
from app.services.auth_service import create_user, login_user, get_user
from app.middleware.auth_middleware import get_current_user


router = APIRouter()

@router.post("/auth/register", response_model=dict)
async def register(user_data: UserData, db: Session = Depends(get_db)):
    return create_user(user_data, db)

@router.post("/auth/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    return login_user(credentials, db)

@router.get("/auth/me", response_model=UserData)
async def get_me(current_user: User = Depends(get_current_user)):
    return get_user(current_user)