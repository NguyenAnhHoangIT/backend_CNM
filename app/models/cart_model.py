from app.models.base_model import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Cart(Base):
    __tablename__ = "Cart"
    
    UserId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), primary_key=True)
    CreateAt = Column(DateTime(6), nullable=False, default=datetime.now)
    UpdateAt = Column(DateTime(6), nullable=True)
    
    user = relationship("User")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = "CartItem"
    
    CartId = Column(String(255), ForeignKey("Cart.UserId", ondelete='CASCADE'), primary_key=True)
    ProductTypeId = Column(Integer, ForeignKey("ProductTypes.Id", ondelete='CASCADE'), primary_key=True)
    Quantity = Column(Integer, nullable=False)
    CreateAt = Column(DateTime(6), nullable=False, default=datetime.now)
    
    cart = relationship("Cart", back_populates="items")
    product_type = relationship("ProductType")
