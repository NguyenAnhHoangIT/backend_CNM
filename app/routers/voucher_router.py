
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.middleware.authenticate import authenticate
from app.models.voucher_model import Voucher
from app.models.user_model import User
from app.schemas.voucher_schema import Voucher as VoucherSchema, VoucherCreate, VoucherUpdate
from app.schemas.base_schema import DataResponse
from datetime import datetime

router = APIRouter()

@router.get("/vouchers", tags=["vouchers"], description="Get all vouchers", response_model=DataResponse[list[VoucherSchema]])
def get_vouchers(db: Session = Depends(get_db)):
    vouchers = db.query(Voucher).all()
    return DataResponse.custom_response(code="200", message="Get all vouchers success", data=vouchers)

@router.get("/vouchers/{voucher_id}", tags=["vouchers"], description="Get voucher by id", response_model=DataResponse[VoucherSchema])
def get_voucher(voucher_id: int, db: Session = Depends(get_db)):
    voucher = db.query(Voucher).filter(Voucher.Id == voucher_id).first()
    if not voucher:
        return DataResponse.custom_response(code="404", message="Voucher not found", data=None)
    return DataResponse.custom_response(code="200", message="Get voucher success", data=voucher)

@router.post("/vouchers", tags=["vouchers"], description="Create new voucher", response_model=DataResponse[VoucherSchema])
def create_voucher(data: VoucherCreate, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    # In a real app, check if user is Admin
    
    new_voucher = Voucher(
        Name=data.Name,
        Description=data.Description,
        Quantity=data.Quantity,
        Discount=data.Discount,
        Status=data.Status,
        CreateAt=datetime.now(),
        UserId=user.Id # Get User Id from token
    )
    
    try:
        db.add(new_voucher)
        db.commit()
        db.refresh(new_voucher)
        return DataResponse.custom_response(code="201", message="Create voucher success", data=new_voucher)
    except Exception as e:
        print(f"Error creating voucher: {e}")
        return DataResponse.custom_response(code="500", message="Create voucher failed", data=None)

@router.put("/vouchers/{voucher_id}", tags=["vouchers"], description="Update voucher", response_model=DataResponse[VoucherSchema])
def update_voucher(voucher_id: int, data: VoucherUpdate, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    voucher = db.query(Voucher).filter(Voucher.Id == voucher_id).first()
    if not voucher:
        return DataResponse.custom_response(code="404", message="Voucher not found", data=None)
    
    if data.Name is not None:
        voucher.Name = data.Name
    if data.Description is not None:
        voucher.Description = data.Description
    if data.Quantity is not None:
        voucher.Quantity = data.Quantity
    if data.Discount is not None:
        voucher.Discount = data.Discount
    if data.Status is not None:
        voucher.Status = data.Status
        
    try:
        db.commit()
        db.refresh(voucher)
        return DataResponse.custom_response(code="200", message="Update voucher success", data=voucher)
    except Exception as e:
        print(f"Error updating voucher: {e}")
        return DataResponse.custom_response(code="500", message="Update voucher failed", data=None)

@router.delete("/vouchers/{voucher_id}", tags=["vouchers"], description="Delete voucher", response_model=DataResponse[None])
def delete_voucher(voucher_id: int, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    voucher = db.query(Voucher).filter(Voucher.Id == voucher_id).first()
    if not voucher:
        return DataResponse.custom_response(code="404", message="Voucher not found", data=None)
        
    try:
        db.delete(voucher)
        db.commit()
        return DataResponse.custom_response(code="200", message="Delete voucher success", data=None)
    except Exception as e:
        print(f"Error deleting voucher: {e}")
        return DataResponse.custom_response(code="500", message="Delete voucher failed", data=None)
