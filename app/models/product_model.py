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

class Product(Base):
    __tablename__ = "Products"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text, nullable=False)
    Description = Column(Text, nullable=False)
    CreateAt = Column(DateTime(6), nullable=False)
    CategoryId = Column(Integer, ForeignKey("Categories.Id", ondelete='CASCADE'), nullable=False)

class ProductImage(Base):
    __tablename__ = "ProductImages"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Url = Column(Text, nullable=False)
    Description = Column(Text, nullable=False)
    ProductId = Column(Integer, ForeignKey("Products.Id", ondelete='CASCADE'), nullable=False)

class ProductLaunch(Base):
    __tablename__ = "ProductLaunchs"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text, nullable=False)
    Description = Column(Text, nullable=False)
    DateStart = Column(DateTime(6), nullable=False)
    DateEnd = Column(DateTime(6), nullable=False)
    ProductId = Column(Integer, ForeignKey("Products.Id", ondelete='CASCADE'), nullable=False, default=0)

class ProductType(Base):
    __tablename__ = "ProductTypes"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text, nullable=False)
    Quantity = Column(Integer, nullable=False)
    ProductLaunchId = Column(Integer, ForeignKey("ProductLaunchs.Id", ondelete='CASCADE'), nullable=False)
    ImageUrl = Column(Text, nullable=True)
    MaxPrice = Column(Numeric(18, 2), nullable=False, default=0.0)
    MinPrice = Column(Numeric(18, 2), nullable=False, default=0.0)

class PriceItem(Base):
    __tablename__ = "PriceItems"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Number = Column(Integer, nullable=False)
    Price = Column(Numeric(18, 2), nullable=False)
    ProductTypeId = Column(Integer, ForeignKey("ProductTypes.Id", ondelete='CASCADE'), nullable=False, default=0)
