from app.models.base_model import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

class Invoice(Base):
    __tablename__ = "Invoices"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), nullable=False)
    Address = Column(Text, nullable=False)
    Status = Column(Integer, nullable=False)
    CreateAt = Column(DateTime(6), nullable=False)
    Deposit = Column(Numeric(18, 2), nullable=False, default=0.0)
    ToTal = Column(Numeric(18, 2), nullable=False, default=0.0)
    PaymentCode = Column(String(255), nullable=False, default='')

class InvoiceItem(Base):
    __tablename__ = "InvoicesItem"
    
    InvoiceId = Column(Integer, ForeignKey("Invoices.Id", ondelete='CASCADE'), primary_key=True)
    ProductTypeId = Column(Integer, ForeignKey("ProductTypes.Id", ondelete='CASCADE'), primary_key=True)
    Quantity = Column(Integer, nullable=False)
    Amount = Column(Numeric(18, 2), nullable=False)
