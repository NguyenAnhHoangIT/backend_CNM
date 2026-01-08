from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# --- Categories ---
class CategoryBase(BaseModel):
    Name: str
    Description: str
    ImageUrl: str
    CreateAt: Optional[datetime] = None
    Status: int = 1

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    Name: Optional[str] = None
    Description: Optional[str] = None
    ImageUrl: Optional[str] = None
    Status: Optional[int] = None


class Category(CategoryBase):
    Id: int
    class Config:
        from_attributes = True

# --- Product Images ---
class ProductImageBase(BaseModel):
    Url: str
    Description: str
    ProductId: Optional[int] = None # Optional for creation within Product

class ProductImageCreate(BaseModel):
    Url: str
    Description: str

class ProductImage(ProductImageBase):
    Id: int
    class Config:
        from_attributes = True

# --- Products ---
class ProductBase(BaseModel):
    Name: str
    Description: str
    CreateAt: datetime
    CategoryId: int
    Status: int = 1

class ProductCreate(ProductBase):
    Images: Optional[List[ProductImageCreate]] = None
    ProductTypes: List["ProductTypeCreate"] = Field(..., min_length=1)

class ProductUpdate(BaseModel):
    Name: Optional[str] = None
    Description: Optional[str] = None
    CategoryId: Optional[int] = None
    Status: Optional[int] = None
    Images: Optional[List[ProductImageCreate]] = None

class Product(ProductBase):
    Id: int
    Images: List[ProductImage] = []
    ProductTypes: List["ProductType"] = []
    class Config:
        from_attributes = True


# --- Product Types ---
class ProductTypeBase(BaseModel):
    Name: str
    Quantity: int
    ImageUrl: Optional[str] = None
    ProductId: int
    Status: int = 1

class ProductTypeCreate(BaseModel):
    Name: str
    Quantity: int
    ImageUrl: Optional[str] = None
    PriceItem: "PriceItemCreate"

class ProductType(ProductTypeBase):
    Id: int
    PriceItem: Optional["PriceItem"] = None
    class Config:
        from_attributes = True

# --- Price Items ---
class PriceItemBase(BaseModel):
    Number: int
    Price: Decimal
    ProductTypeId: int

class PriceItemCreate(BaseModel):
    Number: int
    Price: Decimal
    
class PriceItem(PriceItemBase):
    Id: int
    class Config:
        from_attributes = True
