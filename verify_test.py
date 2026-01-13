import requests

BASE_URL = "http://localhost:8080"
EMAIL = "test_update_me@example.com"
PASSWORD = "NewPassword123!" 

def login():
    resp = requests.post(f"{BASE_URL}/login", json={
        "Email": EMAIL,
        "Password": PASSWORD
    })
    if resp.status_code != 200:
        resp = requests.post(f"{BASE_URL}/login", json={
            "Email": EMAIL,
            "Password": "Password123!" 
        })
    if resp.status_code == 200:
        return resp.json()["data"]["access_token"]
    return None

def verify_test(token):
    print("Testing dummy endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/cart/test", headers=headers)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

if __name__ == "__main__":
    token = login()
    if token:
        verify_test(token)
    else:
        print("Login failed")
