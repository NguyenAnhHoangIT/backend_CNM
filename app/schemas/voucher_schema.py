from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class VoucherCreate(BaseModel):
    Name: str
    Description: Optional[str] = None
    Quantity: int
    Discount: Decimal
    Status: int = 1

class VoucherUpdate(BaseModel):
    Name: Optional[str] = None
    Description: Optional[str] = None
    Quantity: Optional[int] = None
    Discount: Optional[Decimal] = None
    Status: Optional[int] = None

class Voucher(BaseModel):
    Id: int
    Name: str
    Description: Optional[str] = None
    Quantity: int
    Discount: Decimal
    Status: int
    CreateAt: datetime
    UserId: str
    
    class Config:
        from_attributes = True
