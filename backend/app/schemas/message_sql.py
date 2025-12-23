from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class MessageDB(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    # Sender and receiver relationships
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Message content
    content = Column(Text, nullable=False)

    # Optional: Related apartment (if message is about a specific listing)
    apartment_id = Column(Integer, ForeignKey("apartments.id", ondelete="SET NULL"), nullable=True)

    # Read status
    is_read = Column(Boolean, default=False, nullable=False)
    read_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sender = relationship("UserDB", foreign_keys=[sender_id], backref="sent_messages")
    receiver = relationship("UserDB", foreign_keys=[receiver_id], backref="received_messages")
    apartment = relationship("ApartmentDB", backref="messages")

    def __repr__(self):
        return f"<Message {self.id}: {self.sender_id} -> {self.receiver_id}>"