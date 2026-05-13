"""
routes/reportes.py
------------------
Endpoints para alimentar las gráficas analíticas del frontend.
"""
from fastapi import APIRouter, Depends
from typing import List, Dict

from dependencies import get_current_user, get_movimiento_repo
from repositories.movimiento_repository import MovimientoRepository

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes Analíticos"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/gastos-por-categoria")
def get_gastos_por_categoria(
    current_user: dict = Depends(get_current_user),
    repo: MovimientoRepository = Depends(get_movimiento_repo)
):
    """Retorna la suma total gastada dividida por cada categoría para pintar un Pie Chart."""
    return repo.obtener_gastos_por_categoria(current_user["user_id"])
