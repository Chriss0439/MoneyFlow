"""
schemas/dashboard.py
--------------------
Modelos para el endpoint del Dashboard.
"""
from pydantic import BaseModel

class DashboardResponse(BaseModel):
    total_ingresos: float
    total_gastos: float
    saldo_actual: float
