from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class PropertyImageDB(Base):
    __tablename__ = "property_images"

    image_url = Column(String, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.property_id", ondelete="CASCADE"), nullable=False)

    property = relationship("PropertyDB", back_populates="images")
