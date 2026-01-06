import requests
import json
import time

suffix = int(time.time())
base_url = "http://127.0.0.1:8081"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

# 1. Register
print("--- REGISTER ---")
reg_payload = {
  "FullName": "Login Tester",
  "UserName": f"login_{suffix}",
  "Email": f"login_{suffix}@gmail.com",
  "PhoneNumber": "0999888777",
  "AvatarUrl": "http://img.com/avatar.png",
  "TwoFactorEnabled": False,
  "LockoutEnabled": True,
  "Password": "Password123!",
  "ConfirmPassword": "Password123!"
}
try:
    reg_resp = requests.post(f"{base_url}/register", headers=headers, json=reg_payload)
    print(f"Status: {reg_resp.status_code}")
    print(reg_resp.text)
except Exception as e:
    print(f"Register Failed: {e}")
    exit(1)

# 2. Login
print("\n--- LOGIN ---")
login_payload = {
    "Email": f"login_{suffix}@gmail.com",
    "Password": "Password123!"
}
try:
    login_resp = requests.post(f"{base_url}/login", headers=headers, json=login_payload)
    print(f"Status: {login_resp.status_code}")
    print(login_resp.text)
except Exception as e:
    print(f"Login Failed: {e}")
