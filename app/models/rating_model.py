from app.models.base_model import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

class Rating(Base):
    __tablename__ = "Ratings"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Stars = Column(Integer, nullable=False)
    Comment = Column(Text, nullable=True)
    InvoiceId = Column(Integer, ForeignKey("Invoices.Id", ondelete='CASCADE'), nullable=False)
    CreateAt = Column(DateTime(6), nullable=False)
    UpdateAt = Column(DateTime(6), nullable=True)
    DeleteAt = Column(DateTime(6), nullable=True)

class RatingMedia(Base):
    __tablename__ = "RatingMedia"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Url = Column(Text, nullable=False)
    RatingId = Column(Integer, ForeignKey("Ratings.Id", ondelete='CASCADE'), nullable=False)
