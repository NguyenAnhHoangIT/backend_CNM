from app.models.base_model import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class Favorite(Base):
    __tablename__ = "Favorites"
    
    UserId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), primary_key=True)

class FavouriteProduct(Base):
    __tablename__ = "FavouriteProducts"
    
    FavouriteId = Column(String(255), ForeignKey("Favorites.UserId", ondelete='CASCADE'), primary_key=True)
    ProductId = Column(Integer, ForeignKey("Products.Id", ondelete='CASCADE'), primary_key=True)
    CreateAt = Column(DateTime(6), nullable=False, default=datetime(1, 1, 1))
