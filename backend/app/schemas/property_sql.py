from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database.database import Base
from app.schemas.enums import FacilityType, ConstraintType, PropertyStatus


class PropertyDB(Base):
    __tablename__ = "properties"

    property_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String, nullable=False)
    status = Column(Enum(PropertyStatus), nullable=False, default=PropertyStatus.DRAFT)
    street = Column(String, nullable=True)
    zone = Column(String, nullable=True)
    government = Column(String, nullable=True)
    rent = Column(Integer, nullable=False)
    availability_start = Column(DateTime, nullable=True)
    availability_duration = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    facilities = Column(ARRAY(Enum(FacilityType)), nullable=True)
    constraints = Column(ARRAY(Enum(ConstraintType)), nullable=True)

    owner = relationship("UserDB", back_populates="properties")
    images = relationship("PropertyImageDB", back_populates="property", cascade="all, delete-orphan")
    reviews = relationship("ReviewDB", back_populates="property", cascade="all, delete-orphan")
