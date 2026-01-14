from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.middleware.authenticate import authenticate
from app.models.product_model import Category
from app.schemas.product_schema import Category as CategorySchema, CategoryCreate, CategoryUpdate
from app.schemas.base_schema import DataResponse
from app.core.config import settings
from datetime import datetime
from typing import Optional
import cloudinary
import cloudinary.uploader

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("", description="List all categories", response_model=DataResponse[list[CategorySchema]])
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return DataResponse.custom_response(code="200", message="Get categories success", data=categories)

@router.post("", description="Create a new category", response_model=DataResponse[CategorySchema], dependencies=[Depends(authenticate)])
async def create_category(
    Name: str = Form(...),
    Description: str = Form(...),
    Status: int = Form(1),
    Image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(Image.file, folder="categories")
        image_url = upload_result.get("secure_url")

        db_category = Category(
            Name=Name,
            Description=Description,
            ImageUrl=image_url,
            CreateAt=datetime.now(),
            Status=Status
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return DataResponse.custom_response(code="201", message="Create category success", data=db_category)
    except Exception as e:
        print(f"Error: {e}")
        return DataResponse.custom_response(code="500", message="Create category failed", data=None)

@router.put("/{category_id}", description="Update a category", response_model=DataResponse[CategorySchema], dependencies=[Depends(authenticate)])
async def update_category(
    category_id: int, 
    Name: Optional[str] = Form(None),
    Description: Optional[str] = Form(None),
    Status: Optional[int] = Form(None),
    Image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(Category.Id == category_id).first()
    if not category:
        return DataResponse.custom_response(code="404", message="Category not found", data=None)
    
    if Name is not None:
        category.Name = Name
    if Description is not None:
        category.Description = Description
    if Status is not None:
        category.Status = Status
        
    if Image:
        try:
            upload_result = cloudinary.uploader.upload(Image.file, folder="categories")
            category.ImageUrl = upload_result.get("secure_url")
        except Exception as e:
             print(f"Error uploading image: {e}")
             return DataResponse.custom_response(code="500", message="Failed to upload image", data=None)

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
