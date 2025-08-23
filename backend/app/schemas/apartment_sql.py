from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from app.database.database import Base
from sqlalchemy.orm import relationship

class ApartmentDB(Base):

    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description= Column(Text, nullable=True)
    location = Column(String, nullable=False)
    apartment_type = Column(String, nullable=False)
    rent_per_week = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    duration_len = Column(Integer, nullable=True)
    place_accept = Column(String, nullable=False)
    furnishing_type = Column(String, nullable=False)
    is_pathroom_solo = Column(Boolean, nullable=False)
    parking_type = Column(String, nullable=False)
    keywords = Column(ARRAY(String), nullable=True)
    is_active = Column(Boolean, nullable=False)

    # renter_id is a column in the apartments table.
    # ForeignKey("users.id") means it must match a valid id from the users table.
    # This is the “link” that ties an apartment to its renter.
    renter_id = Column(Integer, ForeignKey("users.id"))

    # This tells SQLAlchemy: "I can access the User (renter) who owns this apartment."
    # Example: apartment.renter.first_name
    renter = relationship("UserDB", back_populates="apartments")