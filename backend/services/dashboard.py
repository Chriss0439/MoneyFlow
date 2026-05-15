"""
services/dashboard.py
---------------------
Lógica para el cálculo del resumen financiero del Dashboard.
"""
from schemas.dashboard import DashboardResponse
from repositories.movimiento_repository import MovimientoRepository

def obtener_resumen_financiero(user_id: int, repo: MovimientoRepository) -> DashboardResponse:
    """Obtiene los totales, calcula el saldo actual y el desglose de independencia financiera."""

    totales = repo.obtener_totales_por_usuario(user_id)
    ingresos = totales.get("ingreso", 0.0)
    gastos = totales.get("gasto", 0.0)
    saldo_actual = ingresos - gastos

    # Desglose de independencia financiera
    dependencia = repo.obtener_dependencia_familiar(user_id)
    apoyo_familiar = dependencia.get("apoyo_familiar", 0.0)
    ingresos_propios = dependencia.get("ingresos_propios", 0.0)

    # Calcular porcentajes (evitar división por cero)
    if ingresos > 0:
        pct_dependencia = round((apoyo_familiar / ingresos) * 100, 1)
        pct_propios = round((ingresos_propios / ingresos) * 100, 1)
    else:
        pct_dependencia = 0.0
        pct_propios = 0.0

    return DashboardResponse(
        total_ingresos=ingresos,
        total_gastos=gastos,
        saldo_actual=saldo_actual,
        apoyo_familiar=apoyo_familiar,
        ingresos_propios=ingresos_propios,
        pct_dependencia=pct_dependencia,
        pct_propios=pct_propios,
    )
