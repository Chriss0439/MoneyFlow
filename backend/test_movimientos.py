import requests

BASE_URL = "http://localhost:8000"

print("=== 1. Login ===")
res = requests.post(f"{BASE_URL}/auth/login", json={"correo":"christian@moneyflow.gt", "password":"mipassword123"})
token = res.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}
print(f"Token OK: {token[:20]}...")

print("\n=== 2. Registrar Ingreso ===")
res = requests.post(f"{BASE_URL}/movimientos/", headers=headers, json={
    "categoria_id": 1, "monto": 1500.00, "descripcion": "Mesada de papa", "es_apoyo_familiar": True
})
print(res.json())

print("\n=== 3. Registrar Gasto ===")
res = requests.post(f"{BASE_URL}/movimientos/", headers=headers, json={
    "categoria_id": 5, "monto": 50.00, "descripcion": "Uber a la U"
})
print(res.json())

print("\n=== 4. Test Error Monto Negativo ===")
res = requests.post(f"{BASE_URL}/movimientos/", headers=headers, json={
    "categoria_id": 4, "monto": -10.00, "descripcion": "Café"
})
print(res.status_code, res.json())

print("\n=== 5. Listar Movimientos ===")
res = requests.get(f"{BASE_URL}/movimientos/", headers=headers)
print(res.json())
