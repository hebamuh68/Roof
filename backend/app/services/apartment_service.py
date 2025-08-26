from sqlalchemy.orm import Session
from app.schemas.apartment_sql import ApartmentDB
from app.models.apartment_pyd import ApartmentRequest, ApartmentFilter

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

def delete_apartment(db:Session, apartment_id:int):
    db_apartment = db.query(ApartmentDB).filter(ApartmentDB.id == apartment_id).first()
    if not db_apartment:
        return None
    
    # Delete the apartment
    db.delete(db_apartment)
    db.commit()
    return {"message": "Apartment deleted successfully"}
    

def update_apartment(db:Session, apartment_id:int, apartment_data:ApartmentFilter):
    db_apartment = db.query(ApartmentDB).filter(ApartmentDB.id == apartment_id).first()
    if not db_apartment:
        return None
    
    apartment_clean = apartment_data.model_dump(exclude_unset=True)
    for field, value in apartment_clean.items():
        setattr(db_apartment, field, value)
    
    db.commit()
    db.refresh(db_apartment)
    return db_apartment
