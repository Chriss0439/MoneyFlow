"""
routes/movimientos.py
---------------------
Endpoints para gestionar Movimientos (Ingresos y Gastos).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from schemas.movimientos import MovimientoCreate, MovimientoResponse
from services.movimientos import registrar_movimiento, listar_movimientos_usuario, CategoriaNoExisteError
from dependencies import get_current_user, get_movimiento_repo, get_db
from repositories.movimiento_repository import MovimientoRepository

# Todo el módulo de movimientos requiere usuario logueado
router = APIRouter(
    prefix="/movimientos",
    tags=["Movimientos"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=List[MovimientoResponse])
def get_movimientos(
    mes: int = None,
    anio: int = None,
    categoria_id: int = None,
    current_user: dict = Depends(get_current_user),
    repo: MovimientoRepository = Depends(get_movimiento_repo)
):
    """Obtiene el historial filtrado (opcional) de ingresos y gastos."""
    return listar_movimientos_usuario(current_user["user_id"], repo, mes, anio, categoria_id)


@router.post("/", response_model=MovimientoResponse, status_code=status.HTTP_201_CREATED)
def create_movimiento(
    body: MovimientoCreate,
    current_user: dict = Depends(get_current_user),
    repo: MovimientoRepository = Depends(get_movimiento_repo),
    db: Session = Depends(get_db)
):
    """Registra un nuevo ingreso o gasto para el usuario logueado."""
    try:
        return registrar_movimiento(current_user["user_id"], body, repo, db)
    except CategoriaNoExisteError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{movimiento_id}", status_code=status.HTTP_200_OK)
def delete_movimiento(
    movimiento_id: int,
    current_user: dict = Depends(get_current_user),
    repo: MovimientoRepository = Depends(get_movimiento_repo)
):
    """Elimina permanentemente un movimiento."""
    try:
        from services.movimientos import eliminar_movimiento
        return eliminar_movimiento(current_user["user_id"], movimiento_id, repo)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
