from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RatingMediaBase(BaseModel):
    Url: str
    RatingId: int

class RatingMedia(RatingMediaBase):
    Id: int
    class Config:
        from_attributes = True

class RatingBase(BaseModel):
    Stars: int
    Comment: Optional[str] = None
    InvoiceId: int
    CreateAt: datetime
    UpdateAt: Optional[datetime] = None
    DeleteAt: Optional[datetime] = None

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    Id: int
    RatingMedias: Optional[list[RatingMedia]] = None
    class Config:
        from_attributes = True
