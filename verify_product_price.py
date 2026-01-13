import requests
import json

BASE_URL = "http://localhost:8080"
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

def verify_refactor(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    print("Testing Product Create WITHOUT Number field...")
    payload = {
        "Name": "Refactor Test Product",
        "Description": "Testing Number removal",
        "CategoryId": 1, 
        "CreateAt": "2026-01-01T00:00:00",
        "ProductTypes": [
            {
                "Name": "Type A",
                "Quantity": 10,
                "Price": 50000.0,
                # No Number field
                "ImageUrl": ""
            }
        ]
    }
    
    resp = requests.post(f"{BASE_URL}/products", headers=headers, json=payload)
    print(f"Create status: {resp.status_code}")
    
    if resp.status_code == 201:
        prod = resp.json()["data"]
        print(f"Product Created: {prod['Id']}")
        pt = prod["ProductTypes"][0]
        print(f"ProductType Price: {pt.get('Price')}")
        print(f"ProductType Number (Should be None/Missing): {pt.get('Number')}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/products/{prod['Id']}", headers=headers)
        print("Cleanup done")
    else:
        print(resp.text)

if __name__ == "__main__":
    token = login()
    if token:
        verify_refactor(token)
