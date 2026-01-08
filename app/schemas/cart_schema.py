from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.product_schema import ProductType

class CartItemBase(BaseModel):
    ProductTypeId: int
    Quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    CartId: str
    CreateAt: datetime
    ProductType: Optional[ProductType] = None
    
    class Config:
        from_attributes = True

class CartBase(BaseModel):
    UserId: str

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    CreateAt: datetime
    UpdateAt: Optional[datetime] = None
    items: List[CartItem] = []
    
    class Config:
        from_attributes = True
