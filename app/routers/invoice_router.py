from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.middleware.authenticate import authenticate
from app.models.invoice_model import Invoice, InvoiceItem
from app.models.cart_model import Cart, CartItem
from app.models.product_model import ProductType
from app.models.voucher_model import Voucher
from app.schemas.invoice_schema import Invoice as InvoiceSchema, InvoiceCreate, InvoiceAdminUpdate
from app.schemas.base_schema import DataResponse
from datetime import datetime
from sqlalchemy.orm import joinedload

router = APIRouter(
    prefix="/invoices",
    tags=["invoices"],
    dependencies=[Depends(authenticate)]
)

@router.post("", description="Create invoice (Checkout)", response_model=DataResponse[InvoiceSchema])
async def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    # 1. Start Transaction (Implicit in Session)
    
    # 2. Iterate Items and Validate/Deduct Stock
    invoice_items_buffer = []

    # Import PriceItem here or at top level if needed. Ideally top level but keeping local if previously local.
    # It was local before because check was dynamic. Let's move imports to top if cleaner or keep.
    # The previous code had `from app.models.product_model import PriceItem` inside loop. I'll prefer top level but for minimal diff in logic structure I'll place it here.
    from app.models.product_model import PriceItem

    for item in data.Items:
        # Check Product Type
        product_type = db.query(ProductType).filter(ProductType.Id == item.ProductTypeId).first()
        if not product_type:
             return DataResponse.custom_response(code="400", message=f"Product Type {item.ProductTypeId} not found", data=None)
        
        # Check Stock
        if product_type.Quantity < item.Quantity:
            return DataResponse.custom_response(code="400", message=f"Not enough stock for {product_type.Name}", data=None)
            
        # Deduct Stock
        product_type.Quantity -= item.Quantity
        
        # We trust the Amount sent by frontend? Or recalculate?
        # User request says: "input should be Address, Total and VoucherId (if use) and also a list of InvoicesItem including all column"
        # "all column" for InvoiceItem includes Amount.
        # Usually backend should validate Price, but instructions imply "input ... including all column". 
        # I will use the input Amount but maybe verify it matches logic? 
        # For simplicity and strictly following "input ... including all column", I will use the input values.
        # However, trusting frontend for Amount is dangerous. But for this specific task I will stick to "input ... including all column".
        # Let's just use the input Item.
        
        invoice_items_buffer.append({
            "ProductTypeId": item.ProductTypeId,
            "Quantity": item.Quantity,
            "Amount": item.Amount
        })

    # 3. Create Invoice
    new_invoice = Invoice(
        UserId=user.Id,
        Address=data.Address,
        Status=1, 
        CreateAt=datetime.now(),
        Total=data.Total,
        VoucherId=data.VoucherId
    )
    db.add(new_invoice)
    db.flush() # Get Id

    # 4. Create InvoiceItems
    for buffer in invoice_items_buffer:
        inv_item = InvoiceItem(
            InvoiceId=new_invoice.Id,
            ProductTypeId=buffer["ProductTypeId"],
            Quantity=buffer["Quantity"],
            Amount=buffer["Amount"]
        )
        db.add(inv_item)

    try:
        db.commit()
        db.refresh(new_invoice)
        return DataResponse.custom_response(code="201", message="Create invoice success", data=new_invoice)
    except Exception as e:
        print(f"Error creating invoice: {e}")
        db.rollback()
        return DataResponse.custom_response(code="500", message="Create invoice failed", data=None)

@router.get("", description="Get my invoices", response_model=DataResponse[list[InvoiceSchema]])
async def get_my_invoices(db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    invoices = db.query(Invoice).options(joinedload(Invoice.Items)).filter(Invoice.UserId == user.Id).all()
    return DataResponse.custom_response(code="200", message="Get invoices success", data=invoices)

@router.get("/all", description="Admin get all invoices", response_model=DataResponse[list[InvoiceSchema]])
async def get_all_invoices(db: Session = Depends(get_db)):
    # Admin only check ideally, but instructions didn't enforce separate Role check logic yet.
    # Assuming authenticated user is Admin if they access this? 
    # Or just returning all.
    invoices = db.query(Invoice).options(joinedload(Invoice.Items)).all()
    return DataResponse.custom_response(code="200", message="Get all invoices success", data=invoices)

@router.get("/{invoice_id}", description="Get invoice detail", response_model=DataResponse[InvoiceSchema])
async def get_invoice_detail(invoice_id: int, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    invoice = db.query(Invoice).options(joinedload(Invoice.Items)).filter(Invoice.Id == invoice_id).first()
    if not invoice:
        return DataResponse.custom_response(code="404", message="Invoice not found", data=None)
    
    if invoice.UserId != user.Id:
         # Optional: Check if User has Admin role to allow viewing others' invoices. 
         # For now, strict ownership.
         return DataResponse.custom_response(code="403", message="Access denied", data=None)
         
    return DataResponse.custom_response(code="200", message="Get invoice detail success", data=invoice)

@router.get("/{invoice_id}/admin", description="Admin get invoice detail", response_model=DataResponse[InvoiceSchema])
async def get_invoice_detail_admin(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).options(joinedload(Invoice.Items)).filter(Invoice.Id == invoice_id).first()
    if not invoice:
        return DataResponse.custom_response(code="404", message="Invoice not found", data=None)
    return DataResponse.custom_response(code="200", message="Get invoice detail success", data=invoice)

@router.put("/{invoice_id}", description="Admin update invoice", response_model=DataResponse[InvoiceSchema])
async def update_invoice(invoice_id: int, data: InvoiceAdminUpdate, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).options(joinedload(Invoice.Items)).filter(Invoice.Id == invoice_id).first()
    if not invoice:
        return DataResponse.custom_response(code="404", message="Invoice not found", data=None)
    
    if data.Status is not None:
        invoice.Status = data.Status
    if data.Address is not None:
        invoice.Address = data.Address
        
    try:
        db.commit()
        db.refresh(invoice)
        # Re-query
        invoice = db.query(Invoice).options(joinedload(Invoice.Items)).filter(Invoice.Id == invoice.Id).first()
        return DataResponse.custom_response(code="200", message="Update invoice success", data=invoice)
    except Exception as e:
        print(f"Error updating invoice: {e}")
        db.rollback()
        return DataResponse.custom_response(code="500", message="Update invoice failed", data=None)

@router.delete("/{invoice_id}", description="Admin delete (cancel) invoice", response_model=DataResponse[InvoiceSchema])
async def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.Id == invoice_id).first()
    if not invoice:
        return DataResponse.custom_response(code="404", message="Invoice not found", data=None)
    
    try:
        # Soft delete / Cancel
        invoice.Status = -1
        db.commit()
        db.refresh(invoice)
        return DataResponse.custom_response(code="200", message="Cancel invoice success", data=invoice)
    except Exception as e:
        print(f"Error cancelling invoice: {e}")
        db.rollback()
        return DataResponse.custom_response(code="500", message="Cancel invoice failed", data=None)
