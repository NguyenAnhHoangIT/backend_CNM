from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.middleware.authenticate import authenticate
from app.models.product_model import Category
from app.schemas.product_schema import Category as CategorySchema, CategoryCreate, CategoryUpdate
from app.schemas.base_schema import DataResponse
from datetime import datetime

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("", description="List all categories", response_model=DataResponse[list[CategorySchema]])
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return DataResponse.custom_response(code="200", message="Get categories success", data=categories)

@router.post("", description="Create a new category", response_model=DataResponse[CategorySchema], dependencies=[Depends(authenticate)])
async def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(
        Name=data.Name,
        Description=data.Description,
        ImageUrl=data.ImageUrl,
        CreateAt=datetime.now(),
        Status=data.Status if data.Status else 1
    )
    db.add(db_category)
    try:
        db.commit()
        db.refresh(db_category)
        return DataResponse.custom_response(code="201", message="Create category success", data=db_category)
    except Exception as e:
        print(f"Error: {e}")
        return DataResponse.custom_response(code="500", message="Create category failed", data=None)

@router.put("/{category_id}", description="Update a category", response_model=DataResponse[CategorySchema], dependencies=[Depends(authenticate)])
async def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.Id == category_id).first()
    if not category:
        return DataResponse.custom_response(code="404", message="Category not found", data=None)
    
    if data.Name is not None:
        category.Name = data.Name
    if data.Description is not None:
        category.Description = data.Description
    if data.ImageUrl is not None:
        category.ImageUrl = data.ImageUrl
    if data.Status is not None:
        category.Status = data.Status
        
    try:
        db.commit()
        db.refresh(category)
        return DataResponse.custom_response(code="200", message="Update category success", data=category)
    except Exception as e:
        print(f"Error: {e}")
        return DataResponse.custom_response(code="500", message="Update category failed", data=None)

@router.delete("/{category_id}", description="Delete a category", response_model=DataResponse[CategorySchema], dependencies=[Depends(authenticate)])
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.Id == category_id).first()
    if not category:
        return DataResponse.custom_response(code="404", message="Category not found", data=None)
    
    try:
        db.delete(category)
        db.commit()
        return DataResponse.custom_response(code="200", message="Delete category success", data=None)
    except Exception as e:
        print(e)
        return DataResponse.custom_response(code="500", message="Delete category failed", data=None)
