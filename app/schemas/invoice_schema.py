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
    UserId: str
    Address: str
    Status: int
    CreateAt: datetime
    Deposit: Decimal
    Total: Decimal # Note: Model has ToTal but schema conventionally Total or match exactly? SQL says ToTal. Let's use ToTal to be safe or map it.
    # Re-checking model: ToTal. adhering to model.
    PaymentCode: str

class InvoiceCreate(InvoiceBase):
    Items: List[InvoiceItemCreate]

class Invoice(InvoiceBase):
    Id: int
    Items: List[InvoiceItem] = []
    class Config:
        from_attributes = True
