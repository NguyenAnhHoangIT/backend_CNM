from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.middleware.authenticate import authenticate
from app.models.cart_model import Cart, CartItem
from app.models.product_model import ProductType
from app.schemas.cart_schema import Cart as CartSchema, CartCreate, CartItem as CartItemSchema, CartItemCreate
from app.schemas.base_schema import DataResponse
from datetime import datetime

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
    dependencies=[Depends(authenticate)]
)

@router.get("/me", description="Get current user's cart", response_model=DataResponse[CartSchema])
async def get_my_cart(db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    cart = db.query(Cart).filter(Cart.UserId == user.Id).first()
    if not cart:
        # Create cart if not exists
        cart = Cart(UserId=user.Id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    return DataResponse.custom_response(code="200", message="Get cart success", data=cart)

@router.post("", description="Add item to cart", response_model=DataResponse[CartSchema])
async def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    cart = db.query(Cart).filter(Cart.UserId == user.Id).first()
    if not cart:
        cart = Cart(UserId=user.Id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    # Check if product type exists
    product_type = db.query(ProductType).filter(ProductType.Id == item.ProductTypeId).first()
    if not product_type:
        return DataResponse.custom_response(code="404", message="Product type not found", data=None)

    # Check if item already in cart
    cart_item = db.query(CartItem).filter(CartItem.CartId == cart.UserId, CartItem.ProductTypeId == item.ProductTypeId).first()
    
    if cart_item:
        cart_item.Quantity += item.Quantity
        cart_item.CreateAt = datetime.now() # Update timestamp implies activity? Or maybe add UpdateAt to CartItem
    else:
        cart_item = CartItem(
            CartId=cart.UserId,
            ProductTypeId=item.ProductTypeId,
            Quantity=item.Quantity
        )
        db.add(cart_item)
    
    try:
        db.commit()
        db.refresh(cart)
        return DataResponse.custom_response(code="200", message="Add to cart success", data=cart)
    except Exception as e:
        print(e)
        return DataResponse.custom_response(code="500", message="Add to cart failed", data=None)

@router.put("/items/{product_type_id}", description="Update item quantity", response_model=DataResponse[CartSchema])
async def update_cart_item(product_type_id: int, quantity: int, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    cart = db.query(Cart).filter(Cart.UserId == user.Id).first()
    if not cart:
        return DataResponse.custom_response(code="404", message="Cart not found", data=None)
    
    cart_item = db.query(CartItem).filter(CartItem.CartId == cart.UserId, CartItem.ProductTypeId == product_type_id).first()
    if not cart_item:
        return DataResponse.custom_response(code="404", message="Item not in cart", data=None)
    
    if quantity <= 0:
        db.delete(cart_item)
    else:
        cart_item.Quantity = quantity
        
    db.commit()
    db.refresh(cart)
    return DataResponse.custom_response(code="200", message="Update cart item success", data=cart)

@router.delete("/items/{product_type_id}", description="Remove item from cart", response_model=DataResponse[CartSchema])
async def remove_cart_item(product_type_id: int, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    cart = db.query(Cart).filter(Cart.UserId == user.Id).first()
    if not cart:
        return DataResponse.custom_response(code="404", message="Cart not found", data=None)
    
    cart_item = db.query(CartItem).filter(CartItem.CartId == cart.UserId, CartItem.ProductTypeId == product_type_id).first()
    if not cart_item:
        return DataResponse.custom_response(code="404", message="Item not in cart", data=None)
    
    db.delete(cart_item)
    db.commit()
    db.refresh(cart)
    return DataResponse.custom_response(code="200", message="Remove cart item success", data=cart)
