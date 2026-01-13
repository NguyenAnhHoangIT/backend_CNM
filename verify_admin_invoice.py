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

def verify_invoice_crud(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. List All Invoices
    print(f"\n1. Listing All Invoices...")
    resp = requests.get(f"{BASE_URL}/invoices/all", headers=headers)
    if resp.status_code != 200:
        print(f"List failed: {resp.status_code} - {resp.text}")
        return
    
    invoices = resp.json()["data"]
    print(f"Found {len(invoices)} invoices.")
    if not invoices:
        print("No invoices to test with. Terminating.")
        return

    # Use the first invoice for testing
    invoice_id = invoices[0]["Id"]
    print(f"Using Invoice ID: {invoice_id} for testing")
    
    # 2. Get Invoice Detail (Admin)
    print(f"\n2. Getting Invoice Detail (Admin)...")
    resp = requests.get(f"{BASE_URL}/invoices/{invoice_id}/admin", headers=headers)
    if resp.status_code != 200:
         print(f"Get failed: {resp.status_code} - {resp.text}")
    else:
         print(f"Get success: Invoice {resp.json()['data']['Id']} for {resp.json()['data']['UserId']}")
         
    # 3. Update Invoice
    print(f"\n3. Updating Invoice {invoice_id}...")
    update_payload = {
        "Address": "Updated Admin Address",
        "Status": 2 # Delivering?
    }
    resp = requests.put(f"{BASE_URL}/invoices/{invoice_id}", json=update_payload, headers=headers)
    if resp.status_code != 200:
         print(f"Update failed: {resp.status_code} - {resp.text}")
    else:
         data = resp.json()['data']
         print(f"Update success: Status={data['Status']}, Address={data['Address']}")
         
    # 4. Delete (Cancel) Invoice
    print(f"\n4. Cancelling Invoice {invoice_id}...")
    resp = requests.delete(f"{BASE_URL}/invoices/{invoice_id}", headers=headers)
    if resp.status_code != 200:
         print(f"Delete failed: {resp.status_code} - {resp.text}")
    else:
         print(f"Delete success: Status={resp.json()['data']['Status']}")
         
    # 5. Verify Cancel Status
    print("\n5. Verifying Cancel status...")
    resp = requests.get(f"{BASE_URL}/invoices/{invoice_id}/admin", headers=headers)
    if resp.status_code == 200:
        status = resp.json()['data']['Status']
        if status == -1:
            print("Verification Passed: Invoice status is -1.")
        else:
            print(f"Verification Failed: Invoice status is {status} (Expected -1).")
    else:
         print(f"Get after delete failed: {resp.status_code}")

if __name__ == "__main__":
    token = login()
    if token:
        verify_invoice_crud(token)
