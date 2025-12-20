from app.services.es_client import es
from app.database.database import SessionLocal
from app.schemas.apartment_sql import ApartmentDB
from app.schemas.user_sql import UserDB
from app.models.apartment_pyd import ApartmentRequest


def index_apartments():
    db = SessionLocal()
    apartments = db.query(ApartmentDB).all()

    for apt in apartments:
        apt_data = ApartmentRequest.model_validate(apt).model_dump()
        es.index(index="apartments", id=apt.id, document=apt_data)
    db.close()

if __name__ == "__main__":
    index_apartments()
    print("Apartments indexed to Elasticsearch")
