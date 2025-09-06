import factory
from datetime import datetime, timedelta
from app.schemas.apartment_sql import ApartmentDB

class ApartmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ApartmentDB
        sqlalchemy_session_persistence = "commit"
        
    # Required fields
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    location = factory.Faker("city")
    apartment_type = factory.Iterator(["Studio", "1BHK", "2BHK"])
    rent_per_week = factory.Faker("random_int", min=100, max=2000)
    start_date = factory.LazyFunction(lambda: datetime.utcnow() + timedelta(days=1))
    duration_len = factory.Faker("random_int", min=1, max=52)
    place_accept = factory.Iterator(["Students", "Professionals", "Families"])
    furnishing_type = factory.Iterator(["Furnished", "Unfurnished", "Semi-Furnished"])
    is_pathroom_solo = factory.Faker("boolean")
    parking_type = factory.Iterator(["Garage", "Street", "None"])
    keywords = ["wifi", "balcony", "central heating"]
    is_active = True

    # Foreign key renter_id
    renter_id = factory.Faker("random_int", min=1, max=10)