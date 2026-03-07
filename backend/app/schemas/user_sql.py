from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base


class UserDB(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    dob = Column(DateTime, nullable=True)
    job_title = Column(String, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)

    properties = relationship("PropertyDB", back_populates="owner")
    reviews = relationship("ReviewDB", back_populates="user")
    sent_messages = relationship("MessageDB", foreign_keys="MessageDB.sender_id", back_populates="sender")
    received_messages = relationship("MessageDB", foreign_keys="MessageDB.receiver_id", back_populates="receiver")
    sent_notifications = relationship("NotificationDB", foreign_keys="NotificationDB.sender_id", back_populates="sender")
    received_notifications = relationship("NotificationDB", foreign_keys="NotificationDB.receiver_id", back_populates="receiver")
