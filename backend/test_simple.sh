#!/bin/bash
echo "=== Test Movimientos ==="
RES=$(curl -s -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"correo":"christian@moneyflow.gt","password":"mipassword123"}')
TOKEN=$(echo $RES | grep -o '"access_token":"[^"]*' | grep -o '[^"]*$')

echo "Token: $TOKEN"

echo "Creando ingreso..."
curl -s -X POST http://localhost:8000/movimientos/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"categoria_id": 1, "monto": 1500.00, "descripcion": "Dinero mensual", "es_apoyo_familiar": true}'

echo ""
echo "Creando gasto..."
curl -s -X POST http://localhost:8000/movimientos/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"categoria_id": 5, "monto": 50.00, "descripcion": "Uber", "es_apoyo_familiar": false}'

echo ""
echo "Listando historial..."
curl -s -X GET http://localhost:8000/movimientos/ -H "Authorization: Bearer $TOKEN"
