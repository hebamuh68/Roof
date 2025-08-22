from app.services.es_client import es
from app.database.database import SessionLocal
from app.schemas.apartment import Apartment as ApartmentSchema
from app.models.apartment import Apartment as ApartmentModel


def index_apartments():
    db = SessionLocal()
    apartments = db.query(ApartmentSchema).all()

    for apt in apartments:
        apt_data = ApartmentModel.model_validate(apt).modal_dumb()
        es.index(index="apartments", id=apt.id, body=apt_data)
    db.close()

if __name__ == "__main__":
    index_apartments()
    print("Apartments indexed to Elasticsearch")
