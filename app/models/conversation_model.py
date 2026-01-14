from app.models.base_model import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

class Conversation(Base):
    __tablename__ = "Conversations"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    CustomerId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), nullable=False)
    AdminId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), nullable=False)
    CreatedAt = Column(DateTime(6), nullable=False, default=datetime.now)
    LastMessageAt = Column(DateTime(6), nullable=True, default=datetime.now)

    # Relationships
    Customer = relationship("User", foreign_keys=[CustomerId], backref="customer_conversations")
    Admin = relationship("User", foreign_keys=[AdminId], backref="admin_conversations")
    Messages = relationship("Message", back_populates="Conversation", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('CustomerId', 'AdminId', name='Unique_Chat'),
    )
