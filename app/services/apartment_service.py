from sqlalchemy.orm import Session
from app.schemas.apartment import ApartmentDB


def list_apartment(db: Session, skip:int=0, limit:int=10):
    return db.query(ApartmentDB).offset(skip).limit(limit).all()
