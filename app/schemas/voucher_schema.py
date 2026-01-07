from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class VoucherBase(BaseModel):
    Name: str
    Description: Optional[str] = None
    Quantity: int
    Discount: Decimal
    Status: int
    CreateAt: datetime
    UserId: str

class VoucherCreate(VoucherBase):
    pass

class Voucher(VoucherBase):
    Id: int
    class Config:
        from_attributes = True
