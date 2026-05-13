"""
routes/dashboard.py
-------------------
Capa HTTP para entregar la vista principal de la app.
"""
from fastapi import APIRouter, Depends

from schemas.dashboard import DashboardResponse
from services.dashboard import obtener_resumen_financiero
from dependencies import get_current_user, get_movimiento_repo
from repositories.movimiento_repository import MovimientoRepository

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/resumen", response_model=DashboardResponse)
def get_resumen(
    current_user: dict = Depends(get_current_user),
    repo: MovimientoRepository = Depends(get_movimiento_repo)
):
    """Devuelve los ingresos totales, gastos totales y el saldo actual (Balance)."""
    return obtener_resumen_financiero(current_user["user_id"], repo)
