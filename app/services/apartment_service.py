from sqlalchemy.orm import Session
from app.schemas.apartment_sql import ApartmentDB
from app.models.apartment_pyd import ApartmentRequest

def create_apartment(db: Session, apartment: ApartmentRequest):
    # Convert Pydantic model to SQLAlchemy model
    db_apartment = ApartmentDB(**apartment.model_dump())
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    return db_apartment

def get_apartment_by_id(db: Session, apartment_id: int):
    return db.query(ApartmentDB).filter(ApartmentDB.id == apartment_id).first()

def list_apartments(db: Session, skip:int=0, limit:int=10):
    return db.query(ApartmentDB).offset(skip).limit(limit).all()
