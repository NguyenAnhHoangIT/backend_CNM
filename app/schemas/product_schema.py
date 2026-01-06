from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# --- Categories ---
class CategoryBase(BaseModel):
    Name: str
    Description: str
    ImageUrl: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    Id: int
    class Config:
        from_attributes = True

# --- Products ---
class ProductBase(BaseModel):
    Name: str
    Description: str
    CreateAt: datetime
    CategoryId: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    Id: int
    class Config:
        from_attributes = True

# --- Product Images ---
class ProductImageBase(BaseModel):
    Url: str
    Description: str
    ProductId: int

class ProductImage(ProductImageBase):
    Id: int
    class Config:
        from_attributes = True

# --- Product Launchs ---
class ProductLaunchBase(BaseModel):
    Name: str
    Description: str
    DateStart: datetime
    DateEnd: datetime
    ProductId: int

class ProductLaunch(ProductLaunchBase):
    Id: int
    class Config:
        from_attributes = True

# --- Product Types ---
class ProductTypeBase(BaseModel):
    Name: str
    Quantity: int
    ImageUrl: Optional[str] = None
    MaxPrice: Decimal
    MinPrice: Decimal
    ProductLaunchId: int

class ProductType(ProductTypeBase):
    Id: int
    class Config:
        from_attributes = True

# --- Price Items ---
class PriceItemBase(BaseModel):
    Number: int
    Price: Decimal
    ProductTypeId: int

class PriceItem(PriceItemBase):
    Id: int
    class Config:
        from_attributes = True
