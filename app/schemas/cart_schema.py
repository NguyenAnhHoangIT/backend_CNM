from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Any
from datetime import datetime
from decimal import Decimal


class CartProductType(BaseModel):
    Id: int
    Name: str
    ImageUrl: Optional[str] = None
    Price: Optional[Decimal] = None

    @model_validator(mode='before')
    @classmethod
    def flatten_price_item(cls, data: Any) -> Any:
        try:
            # print(f"Validating CartProductType with data: {data}")
            # Check if data is an ORM object or dict
            if hasattr(data, 'price_item'):
                # print(f"Has price_item: {data.price_item}")
                if data.price_item:
                    # Flatten fields from related object
                    data.Price = data.price_item.Price
                    # print(f"Set Price to: {data.Price}")
        except Exception as e:
            print(f"Validator Error: {e}")
            # raise e # Don't raise, let it fail naturally or return data
        return data

    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    ProductTypeId: int
    Quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    CartId: str
    CreateAt: datetime
    ProductType: Optional[CartProductType] = Field(None, validation_alias="product_type")
    
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
