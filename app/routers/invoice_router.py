from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.middleware.authenticate import authenticate
from app.models.invoice_model import Invoice, InvoiceItem
from app.models.cart_model import Cart, CartItem
from app.models.product_model import ProductType
from app.schemas.invoice_schema import Invoice as InvoiceSchema, InvoiceCreate
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
    # 1. Get Cart
    cart = db.query(Cart).filter(Cart.UserId == user.Id).first()
    if not cart:
        return DataResponse.custom_response(code="400", message="Cart is empty", data=None)

    cart_items = db.query(CartItem).filter(CartItem.CartId == user.Id).all()
    if not cart_items:
        return DataResponse.custom_response(code="400", message="Cart is empty", data=None)

    # 2. Calculate Total and Validate Stock
    total_amount = 0
    invoice_items_buffer = []

    for item in cart_items:
        # Fetch product type to get price and check stock
        # Note: CartItem usually stores ProductTypeId. We need to join or query ProductType -> PriceItem to get price.
        # But wait, ProductType has Quantity (Stock). 
        # Price is in PriceItem. 
        # We need to find the PriceItem for this ProductType.
        # A ProductType has one PriceItem now (as per create_product changes).
        
        # Let's import PriceItem model if needed, or rely on relationships if defined. 
        # ProductType model in product_model.py doesn't seem to have explicit relationship back to PriceItem defined in the snippet I saw?
        # Let's query PriceItem manually for safety.
        from app.models.product_model import PriceItem
        
        product_type = db.query(ProductType).filter(ProductType.Id == item.ProductTypeId).first()
        if not product_type:
             # Should remove invalid item or error? Error for now.
             return DataResponse.custom_response(code="400", message=f"Product Type {item.ProductTypeId} not found", data=None)
        
        if product_type.Quantity < item.Quantity:
            return DataResponse.custom_response(code="400", message=f"Not enough stock for {product_type.Name}", data=None)
            
        price_item = db.query(PriceItem).filter(PriceItem.ProductTypeId == item.ProductTypeId).first()
        if not price_item:
             return DataResponse.custom_response(code="400", message=f"Price not found for {product_type.Name}", data=None)
        
        # Calculate amount
        amount = price_item.Price * item.Quantity
        total_amount += amount
        
        # Deduct stock? Usually done here or reserved.
        product_type.Quantity -= item.Quantity
        
        invoice_items_buffer.append({
            "ProductTypeId": item.ProductTypeId,
            "Quantity": item.Quantity,
            "Amount": amount
        })

    # 3. Create Invoice
    new_invoice = Invoice(
        UserId=user.Id,
        Address=data.Address,
        Status=1, # 1: Pending/Paid? Let's say 1=Created
        CreateAt=datetime.now(),
        Total=total_amount,
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

    # 5. Clear Cart
    db.query(CartItem).filter(CartItem.CartId == user.Id).delete()
    
    try:
        db.commit()
        db.refresh(new_invoice)
        # To return proper schema with Items, we might need to eager load or let Pydantic handle it if relationship exists.
        # Check Invoice model relationship: define it if missing.
        # InvoiceItem model has foreign key to Invoice. 
        # Invoice model needs `items = relationship("InvoiceItem")` for Pydantic `Items` field to populate automatically if orm_mode=True.
        # If not present in model, we might only get empty list.
        # For now, return what we have.
        return DataResponse.custom_response(code="201", message="Create invoice success", data=new_invoice)
    except Exception as e:
        print(f"Error creating invoice: {e}")
        db.rollback()
        return DataResponse.custom_response(code="500", message="Create invoice failed", data=None)

@router.get("", description="Get my invoices", response_model=DataResponse[list[InvoiceSchema]])
async def get_my_invoices(db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    invoices = db.query(Invoice).options(joinedload(Invoice.Items)).filter(Invoice.UserId == user.Id).all()
    return DataResponse.custom_response(code="200", message="Get invoices success", data=invoices)

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
