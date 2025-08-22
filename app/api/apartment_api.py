from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.services.apartment_service import list_apartments, create_apartment, get_apartment_by_id
from app.models.apartment_pyd import ApartmentRequest

router = APIRouter()

# You need to create a new session for each request
# Sessions should be short-lived and closed after use
# DO THIS
def get_db():
    db = SessionLocal()  # New session for each request
    try:
        yield db
    finally:
        db.close()  # Always close the session


@router.post("/apartments")
def create(apartment: ApartmentRequest,db: Session = Depends(get_db)):
    return create_apartment(db,apartment)

@router.get("/apartments/{apartment_id}")
def get(apartment_id: int, db: Session = Depends(get_db)):
    return get_apartment_by_id(db, apartment_id)


@router.get("/apartments")
def list(skip:int=0, limit:int=10, db: Session = Depends(get_db)):
    return list_apartments(db, skip, limit)