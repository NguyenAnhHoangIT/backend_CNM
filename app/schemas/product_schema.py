from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# --- Categories ---
class CategoryBase(BaseModel):
    Name: str
    Description: str
    Name: str
    Description: str
    ImageUrl: str
    CreateAt: Optional[datetime] = None
    Status: int = 1

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
    CreateAt: datetime
    CategoryId: int
    Status: int = 1

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    Name: Optional[str] = None
    Description: Optional[str] = None
    CategoryId: Optional[int] = None
    Status: Optional[int] = None

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
    ImageUrl: Optional[str] = None
    MaxPrice: Decimal
    MinPrice: Decimal
    ProductLaunchId: int
    Status: int = 1

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
