from app.models.base_model import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

class Notification(Base):
    __tablename__ = "Notifications"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(Text, nullable=False)
    Content = Column(Text, nullable=False)
    CreateAt = Column(DateTime(6), nullable=False)
    ReadAt = Column(DateTime(6), nullable=True)
    Status = Column(Integer, nullable=False)
    ReceiverId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), nullable=False)
