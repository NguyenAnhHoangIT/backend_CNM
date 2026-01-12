from fastapi import APIRouter, UploadFile, File, HTTPException
import cloudinary
import cloudinary.uploader
from app.core.config import settings

router = APIRouter()

# Configure Cloudinary
cloudinary.config( 
  cloud_name = settings.CLOUDINARY_CLOUD_NAME, 
  api_key = settings.CLOUDINARY_API_KEY, 
  api_secret = settings.CLOUDINARY_API_SECRET 
)

@router.post("/upload", tags=["upload"], description="Upload an image to Cloudinary")
async def upload_image(file: UploadFile = File(...), folder: str = "smokealot_prods"):
    try:
        # Upload the file to Cloudinary
        result = cloudinary.uploader.upload(file.file, folder=folder)
        return {
            "url": result.get("secure_url"),
            "public_id": result.get("public_id")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")
