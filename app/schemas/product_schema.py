from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Any
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
    Price: Decimal
    Number: int

class ProductType(ProductTypeBase):
    Id: int
    Price: Optional[Decimal] = None
    Number: Optional[int] = None

    @model_validator(mode='before')
    @classmethod
    def flatten_price_item(cls, data: Any) -> Any:
        # Check if data is an ORM object or dict
        if hasattr(data, 'price_item') and data.price_item:
            # Flatten fields from related object
            data.Price = data.price_item.Price
            data.Number = data.price_item.Number
        elif isinstance(data, dict):
            # If dict (e.g. from input or testing), check for nested key (unlikely in this direction but good for robustness)
            pass
        return data

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
