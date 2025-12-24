from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from app.database.database import Base


class NotificationDB(Base):
    """
    Notification model for storing user notifications.

    Attributes:
        id: Primary key
        user_id: Target user who receives the notification
        title: Short notification title
        content: Detailed notification content
        is_read: Whether the notification has been read
        data: JSON field for additional metadata (e.g., message_id, sender_id, type)
        created_at: Timestamp when notification was created
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)
    data = Column(JSON, nullable=True)  # Stores related entity IDs and notification type
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to user
    user = relationship("UserDB", backref="notifications")

    # Indexes are already created in migration
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, title={self.title})>"