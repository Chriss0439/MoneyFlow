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
    # Métricas de independencia financiera
    apoyo_familiar: float       # Monto total de ingresos marcados como apoyo familiar
    ingresos_propios: float     # Monto total de ingresos propios (freelance, trabajo, etc.)
    pct_dependencia: float      # % del total de ingresos que proviene de apoyo familiar
    pct_propios: float          # % del total de ingresos que son propios
