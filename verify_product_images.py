import asyncio
import httpx
import sys
import os

# Add current directory to sys.path to ensure imports work
sys.path.append(os.getcwd())

from app.db.base import engine, SessionLocal
from app.models.product_model import Category

def create_test_category():
    db = SessionLocal()
    try:
        # Check if exists first
        cat = db.query(Category).filter(Category.Name == "Test Category Images").first()
        if not cat:
            cat = Category(
                Name="Test Category Images",
                Description="For Image Testing",
                ImageUrl="http://example.com/cat_img.png",
                Status=1
            )
            db.add(cat)
            db.commit()
            db.refresh(cat)
            print(f"Created Test Category with ID: {cat.Id}")
        else:
            print(f"Using existing Test Category with ID: {cat.Id}")
        return cat.Id
    finally:
        db.close()

def delete_test_category(cat_id):
    db = SessionLocal()
    try:
        cat = db.query(Category).filter(Category.Id == cat_id).first()
        if cat:
            db.delete(cat)
            db.commit()
            print(f"Deleted Test Category with ID: {cat_id}")
    finally:
        db.close()

async def verify_images():
    base_url = "http://127.0.0.1:8000"
    
    cat_id = create_test_category()

    async with httpx.AsyncClient(base_url=base_url) as client:
        # 1. Create Product with Images
        print("\n--- Testing Create Product with Images ---")
        product_data = {
            "Name": "Product With Images",
            "Description": "Has 2 images",
            "CategoryId": cat_id,
            "CreateAt": "2023-01-01T00:00:00",
            "Status": 1,
            "Images": [
                {"Url": "http://img1.com", "Description": "Image 1"},
                {"Url": "http://img2.com", "Description": "Image 2"}
            ]
        }
        
        response = await client.post("/products", json=product_data)
        resp_json = response.json()
        
        if response.status_code != 200 or resp_json.get('code') != "201":
            print(f"Failed to create product. Status: {response.status_code}, Body: {response.text}")
            delete_test_category(cat_id)
            return

        created_product = resp_json['data']
        product_id = created_product['Id']
        print(f"Created Product ID: {product_id}")
        
        # Verify Images in Create Response
        images = created_product.get('Images')
        if images and len(images) == 2:
            print(f"Create Response has {len(images)} images: OK")
        else:
            print(f"Create Response has {len(images) if images else 0} images: FAIL")

        # 2. Get Product
        print("\n--- Testing Get Product ---")
        response = await client.get(f"/products/{product_id}")
        resp_json = response.json()
        if response.status_code != 200 or resp_json.get('code') != "200":
             print(f"Failed to get product. Status: {response.status_code}")
        else:
             fetched_product = resp_json['data']
             images = fetched_product.get('Images')
             if images and len(images) == 2:
                 print(f"Get Response has {len(images)} images: OK")
                 print(f"Image 1 URL: {images[0]['Url']}")
             else:
                 print(f"Get Response has {len(images) if images else 0} images: FAIL")

        # 3. Delete Product
        print("\n--- Testing Delete Product ---")
        await client.delete(f"/products/{product_id}")
        print("Deleted Product")

    delete_test_category(cat_id)

if __name__ == "__main__":
    asyncio.run(verify_images())
