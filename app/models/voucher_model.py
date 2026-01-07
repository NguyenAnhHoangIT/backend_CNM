from app.models.base_model import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship

class Voucher(Base):
    __tablename__ = "Vouchers"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Description = Column(Text, nullable=True)
    Quantity = Column(Integer, nullable=False)
    Discount = Column(Numeric(18, 2), nullable=False)
    Status = Column(Integer, nullable=False)
    CreateAt = Column(DateTime(6), nullable=False)
    UserId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), nullable=False)
