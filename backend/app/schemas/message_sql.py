from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database.database import Base


class MessageDB(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    sender = relationship("UserDB", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("UserDB", foreign_keys=[receiver_id], back_populates="received_messages")
