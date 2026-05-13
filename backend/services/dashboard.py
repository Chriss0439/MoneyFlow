"""
services/dashboard.py
---------------------
Lógica para el cálculo del resumen financiero del Dashboard.
"""
from schemas.dashboard import DashboardResponse
from repositories.movimiento_repository import MovimientoRepository

def obtener_resumen_financiero(user_id: int, repo: MovimientoRepository) -> DashboardResponse:
    """Obtiene los totales y calcula el saldo actual."""
    
    totales = repo.obtener_totales_por_usuario(user_id)
    
    ingresos = totales.get("ingreso", 0.0)
    gastos = totales.get("gasto", 0.0)
    saldo_actual = ingresos - gastos
    
    return DashboardResponse(
        total_ingresos=ingresos,
        total_gastos=gastos,
        saldo_actual=saldo_actual
    )
