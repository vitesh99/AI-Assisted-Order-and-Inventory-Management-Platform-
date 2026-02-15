import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1" # Points to Gateway

def seed():
    print("--- Starting Data Seed (Modular Monolith) ---")
    
    # 1. Create User
    print("\n1. Creating Admin User...")
    try:
        register_url = f"{BASE_URL}/auth/signup"
        admin_data = {"email": "admin@example.com", "password": "adminpassword"}
        # Try login first to see if exists
        login_resp = requests.post(f"{BASE_URL}/auth/login", data={"username": "admin@example.com", "password": "adminpassword"})
        
        if login_resp.status_code == 200:
            print("   User already exists. Logging in...")
            token = login_resp.json()['access_token']
        else:
            requests.post(register_url, json=admin_data)
            login_resp = requests.post(f"{BASE_URL}/auth/login", data={"username": "admin@example.com", "password": "adminpassword"})
            token = login_resp.json()['access_token']
            print("   User created and logged in.")
            
        headers = {"Authorization": f"Bearer {token}"}
    except Exception as e:
        print(f"!!! Error creating user: {e}")
        return

    # 2. Create Suppliers (New)
    print("\n2. Creating Suppliers...")
    supplier_ids = []
    suppliers = [
        {"name": "Global Tech Imports", "contact_email": "supply@globaltech.com"},
        {"name": "Local widgets Co", "contact_email": "widgets@local.com"}
    ]
    
    for s in suppliers:
        # We don't have a lookup endpoint easily, so just try create.
        # In real app, we'd check existence. Here we just POST.
        # If duplicated, might fail if unique constraint? We didn't add unique to name.
        resp = requests.post(f"{BASE_URL}/suppliers/", json=s, headers=headers)
        if resp.status_code in [200, 201]:
             supplier_ids.append(resp.json()['id'])
             print(f"   Created Supplier: {s['name']}")
        else:
             # Assume exists or error
             print(f"   Skipped Supplier {s['name']} (Status {resp.status_code})")

    # 3. Create Products
    print("\n3. Creating Inventory...")
    products = [
        {"name": "AI Processor Unit", "price": 45000.0, "stock_quantity": 50, "description": "High performance AI chip"},
        {"name": "Quantum Sensor", "price": 12000.0, "stock_quantity": 5, "description": "Precision sensor"},
        {"name": "Holographic Display", "price": 25000.0, "stock_quantity": 15, "description": "3D visualization unit"},
        {"name": "Neural Interface Headset", "price": 8500.0, "stock_quantity": 100, "description": "Brain-computer interface"},
        {"name": "Smart Battery Pack", "price": 1500.0, "stock_quantity": 200, "description": "Long life energy source"}
    ]

    product_ids = []
    for i, p in enumerate(products):
        # Assign supplier round-robin
        if supplier_ids:
            p['supplier_id'] = supplier_ids[i % len(supplier_ids)]
            
        resp = requests.post(f"{BASE_URL}/inventory/", json=p, headers=headers)
        if resp.status_code == 200:
            product_ids.append(resp.json()['id'])
            print(f"   Created: {p['name']}")
        else:
            print(f"   Failed to create {p['name']}: {resp.status_code} - {resp.text}")

    # 4. Create Orders
    print("\n4. Creating Seed Orders...")
    orders_data = [
        {"items": [{"product_id": product_ids[0], "quantity": 2}, {"product_id": product_ids[4], "quantity": 10}]},
        {"items": [{"product_id": product_ids[1], "quantity": 1}]},
        {"items": [{"product_id": product_ids[2], "quantity": 2}]},
        {"items": [{"product_id": product_ids[3], "quantity": 5}]}
    ]

    for order in orders_data:
        try:
            resp = requests.post(f"{BASE_URL}/orders/", json=order, headers=headers)
            if resp.status_code == 200:
                print(f"   Created Order ID: {resp.json()['id']}")
            else:
                 print(f"   Failed Order: {resp.text}")
        except IndexError:
            pass

    print("\n--- Seeding Complete ---")
    print(f"Admin Credentials: admin@example.com / adminpassword")

if __name__ == "__main__":
    try:
        seed()
    except Exception as e:
        print(f"Seed failed: {e}. Is the backend running at {BASE_URL}?")
