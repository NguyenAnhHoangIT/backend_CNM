from app.models.base_model import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

class Category(Base):
    __tablename__ = "Categories"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text, nullable=False)
    Description = Column(Text, nullable=False)
    ImageUrl = Column(Text, nullable=False)
    CreateAt = Column(DateTime(6), nullable=False, default=datetime.now)
    Status = Column(Integer, nullable=False, default=1)

class Product(Base):
    __tablename__ = "Products"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text, nullable=False)
    Description = Column(Text, nullable=False)
    CreateAt = Column(DateTime(6), nullable=False)
    Status = Column(Integer, nullable=False, default=1)
    CategoryId = Column(Integer, ForeignKey("Categories.Id", ondelete='CASCADE'), nullable=False)
    
    # Relationships
    Images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    ProductTypes = relationship("ProductType", back_populates="product", cascade="all, delete-orphan")

class ProductImage(Base):
    __tablename__ = "ProductImages"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Url = Column(Text, nullable=False)
    Description = Column(Text, nullable=False)
    ProductId = Column(Integer, ForeignKey("Products.Id", ondelete='CASCADE'), nullable=False)
    
    product = relationship("Product", back_populates="Images")


class ProductType(Base):
    __tablename__ = "ProductTypes"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text, nullable=False)
    Quantity = Column(Integer, nullable=False)
    Status = Column(Integer, nullable=False, default=1)
    ProductId = Column(Integer, ForeignKey("Products.Id", ondelete='CASCADE'), nullable=False)
    ImageUrl = Column(Text, nullable=True)
    
    product = relationship("Product", back_populates="ProductTypes")
    price_item = relationship("PriceItem", uselist=False, backref="product_type", cascade="all, delete-orphan")

class PriceItem(Base):
    __tablename__ = "PriceItem"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Number = Column(Integer, nullable=False)
    Price = Column(Numeric(18, 2), nullable=False)
    ProductTypeId = Column(Integer, ForeignKey("ProductTypes.Id", ondelete='CASCADE'), nullable=False, default=0)
