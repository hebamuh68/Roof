from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
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

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sender = relationship("UserDB", foreign_keys=[sender_id], backref="sent_messages")
    receiver = relationship("UserDB", foreign_keys=[receiver_id], backref="received_messages")

    def __repr__(self):
        return f"<Message {self.id}: {self.sender_id} -> {self.receiver_id}>"