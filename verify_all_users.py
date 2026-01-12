
import requests
import json
import uuid

base_url = "http://127.0.0.1:8080"
unique_str = str(uuid.uuid4())[:8]

def verify_all_users():
    print("--- Verify GET /users ---")
    
    # 1. Login
    email = f"list_{unique_str}@example.com"
    password = "password123"
    
    requests.post(f"{base_url}/register", json={
        "FullName": "List User", "Email": email, "UserName": f"list_{unique_str}", 
        "Password": password, "ConfirmPassword": password
    })
    res = requests.post(f"{base_url}/login", json={"Email": email, "Password": password})
    if res.status_code != 200:
        print("Login failed")
        return
    token = res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get All Users
    res = requests.get(f"{base_url}/users", headers=headers)
    print(f"GET /users: {res.status_code}")
    
    if res.status_code == 200:
        data = res.json()["data"]
        print(f"Count: {len(data)}")
        if len(data) > 0:
            user_0 = data[0]
            # Verify it has detailed info (UserSchema fields)
            print(f"User[0] Keys: {user_0.keys()}")
            if "Roles" in user_0:
                print("SUCCESS: Roles present in list")
            else:
                print("FAILURE: Roles missing")
    else:
        print(f"FAILURE: {res.text}")

verify_all_users()
