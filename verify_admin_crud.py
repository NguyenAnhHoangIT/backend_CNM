import requests
import json
import random

BASE_URL = "http://localhost:8080"
EMAIL = "hoang3@gmail.com"
PASSWORD = "string"

def login():
    print(f"Logging in with {EMAIL}...")
    try:
        resp = requests.post(f"{BASE_URL}/login", json={
            "Email": EMAIL,
            "Password": PASSWORD
        })
        if resp.status_code == 200:
            token = resp.json()["data"]["access_token"]
            print("Login successful.")
            return token
        else:
            print(f"Login failed: {resp.status_code} - {resp.text}")
            return None
    except Exception as e:
        print(f"Login exception: {e}")
        return None

def verify_crud(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    # Generate random email to avoid duplicate errors on re-runs
    rand_id = random.randint(1000, 9999)
    new_user_email = f"testadmin{rand_id}@example.com"
    
    # 1. Create User
    print(f"\n1. Creating User {new_user_email}...")
    create_payload = {
        "FullName": "Test Admin User",
        "Email": new_user_email,
        "Password": "Password123!",
        "UserName": f"testadmin{rand_id}",
        "PhoneNumber": "1234567890",
        "Status": 1
    }
    resp = requests.post(f"{BASE_URL}/users", json=create_payload, headers=headers)
    if resp.status_code not in [200, 201]:
        print(f"Create failed: {resp.status_code} - {resp.text}")
        return
    
    user_data = resp.json()["data"]
    user_id = user_data["Id"]
    print(f"User created: Id={user_id}, Name={user_data['FullName']}")
    
    # 2. Get User
    print("\n2. Getting User details...")
    resp = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
    if resp.status_code != 200:
         print(f"Get failed: {resp.status_code} - {resp.text}")
    else:
         print(f"Get success: {resp.json()['data']['Email']}")
         
    # 3. Update User
    print("\n3. Updating User...")
    update_payload = {
        "FullName": "Updated Admin User",
        "Status": 1
    }
    resp = requests.put(f"{BASE_URL}/users/{user_id}", json=update_payload, headers=headers)
    if resp.status_code != 200:
         print(f"Update failed: {resp.status_code} - {resp.text}")
    else:
         print(f"Update success: {resp.json()['data']['FullName']}")
         
    # 4. Delete User (Soft Delete)
    print("\n4. Deleting User (Soft Delete)...")
    resp = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    if resp.status_code != 200:
         print(f"Delete failed: {resp.status_code} - {resp.text}")
    else:
         print(f"Delete success: {resp.json()['data']['Status']}")
         
    # 5. Verify Soft Delete
    print("\n5. Verifying Soft Delete status...")
    resp = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
    if resp.status_code == 200:
        status = resp.json()['data']['Status']
        if status == 0:
            print("Verification Passed: User status is 0.")
        else:
            print(f"Verification Failed: User status is {status} (Expected 0).")
    else:
        print(f"Get after delete failed: {resp.status_code}")

if __name__ == "__main__":
    token = login()
    if token:
        verify_crud(token)
