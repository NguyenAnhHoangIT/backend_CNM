from fastapi import APIRouter, Depends, File, UploadFile, Form
from app.middleware.authenticate import authenticate
from app.db.base import get_db
from app.db.base import get_db
from sqlalchemy.orm import Session, joinedload
from app.models.product_model import Product, Category, ProductImage, ProductType, PriceItem
from app.schemas.product_schema import Product as ProductSchema, ProductCreate, ProductUpdate
from app.schemas.base_schema import DataResponse
from app.core.config import settings
from datetime import datetime
from typing import List, Optional
import cloudinary
import cloudinary.uploader
import json

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

router = APIRouter()

@router.get("/products", tags=["products"], description="Get all products", response_model=DataResponse[list[ProductSchema]])
async def get_products(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    products = db.query(Product).options(joinedload(Product.ProductTypes).joinedload(ProductType.price_item), joinedload(Product.Images)).offset(skip).limit(limit).all()
    # Pydantic with from_attributes=True should handle getting PascalCase fields from Model and outputting PascalCase JSON
    return DataResponse.custom_response(code="200", message="get list products", data=products)

# ... (create_product remains same, manual add works)

@router.get("/products/{product_id}", tags=["products"], description="Get a product by id", response_model=DataResponse[ProductSchema])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).options(joinedload(Product.ProductTypes).joinedload(ProductType.price_item), joinedload(Product.Images)).filter(Product.Id == product_id).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    return DataResponse.custom_response(code="200", message="Get product by id", data=product)

@router.post("/products", tags=["products"], description="Create a new product", response_model=DataResponse[ProductSchema])
async def create_product(
    Name: str = Form(...),
    Description: Optional[str] = Form(None),
    CategoryId: int = Form(...),
    Status: int = Form(1),
    Images: List[UploadFile] = File(...),
    ProductTypeNames: List[str] = Form(...),
    ProductTypeQuantities: List[int] = Form(...),
    ProductTypePrices: List[str] = Form(...),
    ProductTypeImages: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(authenticate)
):
    try:
        # Validate all ProductType arrays have same length
        if not (len(ProductTypeNames) == len(ProductTypeQuantities) == len(ProductTypePrices) == len(ProductTypeImages)):
            return DataResponse.custom_response(
                code="400", 
                message="All ProductType arrays must have the same length", 
                data=None
            )
        
        # Create Product
        db_product = Product(
            Name=Name,
            Description=Description or "",
            CreateAt=datetime.now(),
            CategoryId=CategoryId,
            Status=Status
        )
        db.add(db_product)
        db.flush()  # Get product Id

        # Upload and create Product Images
        if Images:
            for img_file in Images:
                upload_result = cloudinary.uploader.upload(img_file.file, folder="products")
                image_url = upload_result.get("secure_url")
                
                db_image = ProductImage(
                    Url=image_url,
                    Description=img_file.filename or "Product image",
                    ProductId=db_product.Id
                )
                db.add(db_image)
        
        # Create ProductTypes
        for i in range(len(ProductTypeNames)):
            # Upload ProductType image
            pt_image_url = None
            if ProductTypeImages[i]:
                upload_result = cloudinary.uploader.upload(ProductTypeImages[i].file, folder="product_types")
                pt_image_url = upload_result.get("secure_url")
            
            db_product_type = ProductType(
                Name=ProductTypeNames[i],
                Quantity=ProductTypeQuantities[i],
                ImageUrl=pt_image_url,
                ProductId=db_product.Id,
                Status=1
            )
            db.add(db_product_type)
            db.flush()  # Get ProductType Id
            
            # Create PriceItem
            db_price_item = PriceItem(
                Number=0,
                Price=ProductTypePrices[i],
                ProductTypeId=db_product_type.Id
            )
            db.add(db_price_item)

        db.commit()
        db.refresh(db_product)
        
        # Reload with relationships
        product = db.query(Product).options(
            joinedload(Product.ProductTypes).joinedload(ProductType.price_item),
            joinedload(Product.Images)
        ).filter(Product.Id == db_product.Id).first()
        
        return DataResponse.custom_response(code="201", message="Create product success", data=product)
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return DataResponse.custom_response(code="500", message=f"Create product failed: {str(e)}", data=None)



@router.put("/products/{product_id}", tags=["products"], description="Update a product by id", response_model=DataResponse[ProductSchema])
async def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    product = db.query(Product).filter(Product.Id == product_id).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    
    if data.Name is not None:
        product.Name = data.Name
    if data.Description is not None:
        product.Description = data.Description
    if data.CategoryId is not None:
        product.CategoryId = data.CategoryId
    if data.Status is not None:
        product.Status = data.Status
        
    try:
        db.commit()
        db.refresh(product)
        return DataResponse.custom_response(code="200", message="Update product success", data=product)
    except Exception as e:
        print(f"Error: {e}")
        return DataResponse.custom_response(code="500", message="Update product failed", data=None)

@router.delete("/products/{product_id}", tags=["products"], description="Delete a product by id", response_model=DataResponse[ProductSchema])
def delete_product(product_id: int, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    product = db.query(Product).filter(Product.Id == product_id).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    
    db.delete(product)
    db.commit()
    return DataResponse.custom_response(code="200", message="Delete product by id", data=None)
