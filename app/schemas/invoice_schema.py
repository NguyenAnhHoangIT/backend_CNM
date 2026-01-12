from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# --- Invoice Items ---
class InvoiceItemBase(BaseModel):
    ProductTypeId: int
    Quantity: int
    Amount: Decimal

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItem(InvoiceItemBase):
    InvoiceId: int
    class Config:
        from_attributes = True

# --- Invoices ---
class InvoiceBase(BaseModel):
    Address: str
    Status: int = 1
    CreateAt: Optional[datetime] = None
    Total: Decimal = Decimal(0)
    VoucherId: Optional[int] = None

class InvoiceCreate(BaseModel):
    Address: str
class InvoiceCreate(BaseModel):
    Address: str
    VoucherName: Optional[str] = None

class Invoice(InvoiceBase):
    Id: int
    UserId: str
    Items: List[InvoiceItem] = []
    class Config:
        from_attributes = True
