from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class ReviewDB(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.property_id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=True)
    stars = Column(Integer, nullable=False)

    user = relationship("UserDB", back_populates="reviews")
    property = relationship("PropertyDB", back_populates="reviews")
