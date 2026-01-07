from fastapi import APIRouter, Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.product_model import Product, Category, ProductImage
from app.schemas.product_schema import Product as ProductSchema, ProductCreate, ProductUpdate
from app.schemas.base_schema import DataResponse
from datetime import datetime

router = APIRouter()

@router.get("/products", tags=["products"], description="Get all products", response_model=DataResponse[list[ProductSchema]])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    # Pydantic with from_attributes=True should handle getting PascalCase fields from Model and outputting PascalCase JSON
    return DataResponse.custom_response(code="200", message="get list products", data=products)

@router.post("/products", tags=["products"], description="Create a new product", response_model=DataResponse[ProductSchema])
async def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    # Accessing PascalCase fields from data
    db_product = Product(
        Name=data.Name,
        Description=data.Description,
        CreateAt=datetime.now(), # or data.CreateAt if passed
        CategoryId=data.CategoryId,
        Status=data.Status if data.Status else 1
    )
    try:
        db.add(db_product)
        db.flush() # Flush to get db_product.Id

        if data.Images:
            for img in data.Images:
                db_image = ProductImage(
                    Url=img.Url,
                    Description=img.Description,
                    ProductId=db_product.Id
                )
                db.add(db_image)

        db.commit()
        db.refresh(db_product)
        return DataResponse.custom_response(code="201", message="Create product success", data=db_product)
    except Exception as e:
        print(f"Error: {e}")
        return DataResponse.custom_response(code="500", message="Create product failed", data=None)

@router.get("/products/{product_id}", tags=["products"], description="Get a product by id", response_model=DataResponse[ProductSchema])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.Id == product_id).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    return DataResponse.custom_response(code="200", message="Get product by id", data=product)

@router.put("/products/{product_id}", tags=["products"], description="Update a product by id", response_model=DataResponse[ProductSchema])
async def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
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
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.Id == product_id).first()
    if not product:
        return DataResponse.custom_response(code="404", message="Product not found", data=None)
    
    db.delete(product)
    db.commit()
    return DataResponse.custom_response(code="200", message="Delete product by id", data=None)
