from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FavouriteProductBase(BaseModel):
    ProductId: int
    CreateAt: datetime = datetime.now()

class FavouriteProduct(FavouriteProductBase):
    FavouriteId: str 
    class Config:
        from_attributes = True

class FavoriteBase(BaseModel):
    UserId: str

class Favorite(FavoriteBase):
    Products: List[FavouriteProduct] = []
    class Config:
        from_attributes = True
