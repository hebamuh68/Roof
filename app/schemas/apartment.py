from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from app.database.database import Base

class Apartment(Base):

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