import requests
import json

BASE_URL = "http://localhost:8081"
EMAIL = "test_update_me@example.com"
PASSWORD = "NewPassword123!" 

def login():
    resp = requests.post(f"{BASE_URL}/login", json={
        "Email": EMAIL,
        "Password": PASSWORD
    })
    # Safe fallback
    if resp.status_code != 200:
        resp = requests.post(f"{BASE_URL}/login", json={
            "Email": EMAIL,
            "Password": "Password123!" 
        })
    if resp.status_code == 200:
        return resp.json()["data"]["access_token"]
    return None

def verify_cart(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Ensure we have a product type to add
    print("Creating temporary product...")
    payload = {
        "Name": "Cart Test Product",
        "Description": "Testing Cart",
        "CategoryId": 1, 
        "CreateAt": "2026-01-01T00:00:00",
        "ProductTypes": [
            {
                "Name": "Cart Type",
                "Quantity": 10,
                "Price": 99000.0,
                "ImageUrl": ""
            }
        ]
    }
    
    prod_resp = requests.post(f"{BASE_URL}/products", headers=headers, json=payload)
    if prod_resp.status_code == 200 and prod_resp.json().get("code") == "201":
         product_id = prod_resp.json()["data"]["Id"]
         product_type_id = prod_resp.json()["data"]["ProductTypes"][0]["Id"]
         print(f"Created ProductType ID: {product_type_id}")
    else:
        print(f"Failed to create product: {prod_resp.text}")
        return

    # 2. Add to Cart
    print("Adding to Cart...")
    cart_item = {
        "ProductTypeId": product_type_id,
        "Quantity": 2
    }
    cart_resp = requests.post(f"{BASE_URL}/cart", headers=headers, json=cart_item)
    print(f"Add to cart status: {cart_resp.status_code}")

    # 3. Get Cart
    print("Getting Cart Details...")
    get_resp = requests.get(f"{BASE_URL}/cart/me", headers=headers)
    print(f"Get cart status: {get_resp.status_code}")
    
    if get_resp.status_code == 200:
        print(f"Response JSON: {get_resp.json()}")
        cart_data = get_resp.json()["data"]
        items = cart_data["items"]
        print(f"Items in cart: {len(items)}")
        
        found = False
        for item in items:
            if item["ProductTypeId"] == product_type_id:
                found = True
                print("Found added item:")
                print(f"  Quantity: {item['Quantity']}")
                print(f"  ProductType Name: {item['ProductType']['Name']}")
                print(f"  ProductType Price: {item['ProductType']['Price']}")
                if item['ProductType']['Price'] == '99000.00' or item['ProductType']['Price'] == 99000.0:
                     print("  SUCCESS: Price is correct!")
                else:
                     print(f"  WARNING: Price mismatch (Expected 99000.0)")
        
        if not found:
            print("ERROR: Added item not found in cart response!")
    else:
        print(get_resp.text)

    # Cleanup
    requests.delete(f"{BASE_URL}/products/{product_id}", headers=headers)
    # Cart item requires manual cleanup or ignore (cascade delete might handle it if product is deleted?)
    # Model says: CartItem->ProductType (ForeignKey ondelete='CASCADE')
    # So deleting product -> delete product type -> delete cart item. Should be fine.
    print("Cleanup done")

if __name__ == "__main__":
    token = login()
    if token:
        verify_cart(token)
