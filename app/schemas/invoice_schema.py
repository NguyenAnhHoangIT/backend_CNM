from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# --- Invoice Items ---
class InvoiceItemBase(BaseModel):
    ProductTypeId: int
    Quantity: int
    Amount: Decimal

class InvoiceItemCreate(BaseModel):
    ProductTypeId: int
    Quantity: int
    Amount: Decimal

class InvoiceItem(InvoiceItemBase):
    InvoiceId: int
    ProductName: Optional[str] = None
    ProductTypeName: Optional[str] = None
    ProductTypeImageUrl: Optional[str] = None
    
    class Config:
        from_attributes = True

# --- Invoices ---
class InvoiceBase(BaseModel):
    Address: str
    Status: int = 1
    CreateAt: Optional[datetime] = None
    Total: Decimal = Decimal(0)
    VoucherId: Optional[int] = None
    PaymentIntentId: Optional[str] = None
    Notes: Optional[str] = None

class InvoiceAdminUpdate(BaseModel):
    Status: Optional[int] = None
    Address: Optional[str] = None
    Notes: Optional[str] = None

class InvoiceCreate(BaseModel):
    Address: str
    VoucherId: Optional[int] = None
    Notes: Optional[str] = None
    Items: List[InvoiceItemCreate]

class Invoice(InvoiceBase):
    Id: int
    UserId: str
    Items: List[InvoiceItem] = []
    class Config:
        from_attributes = True

class InvoiceCreateResponse(Invoice):
    ClientSecret: str
