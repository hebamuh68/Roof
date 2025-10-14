from sqlalchemy import Column, Integer, String, Enum, DateTime
from app.database.database import Base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class UserType(enum.Enum):
    SEEKER = "SEEKER"
    RENTER = "RENTER"

class UserDB(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=False)
    flatmate_pref = Column(ARRAY(String), nullable=True)
    keywords = Column(ARRAY(String), nullable=True)
    role = Column(Enum(UserType), nullable=False, default=UserType.SEEKER)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    apartments = relationship("ApartmentDB", back_populates="renter")
