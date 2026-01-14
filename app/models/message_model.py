from app.models.base_model import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class Message(Base):
    __tablename__ = "Messages"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    ConversationId = Column(Integer, ForeignKey("Conversations.Id", ondelete='CASCADE'), nullable=False)
    SenderId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), nullable=False)
    Content = Column(Text, nullable=False)
    MessageType = Column(String(50), default='text') # 'text', 'image', 'system'
    IsRead = Column(Boolean, nullable=False, default=False)
    CreatedAt = Column(DateTime(6), nullable=False, default=datetime.now)

    # Relationships
    Conversation = relationship("Conversation", back_populates="Messages")
    Sender = relationship("User", foreign_keys=[SenderId])
