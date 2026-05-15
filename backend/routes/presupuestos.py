"""
routes/presupuestos.py
----------------------
Endpoints HTTP para el módulo de Presupuestos con Alertas.
"""
from fastapi import APIRouter, Depends, HTTPException

from schemas.presupuestos import PresupuestoCreate, PresupuestoResponse, AlertaPresupuesto
from services.presupuestos import listar_presupuestos, obtener_alertas
from repositories.presupuesto_repository import PresupuestoRepository
from dependencies import get_current_user, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/presupuestos",
    tags=["Presupuestos"],
    dependencies=[Depends(get_current_user)],
)


def get_presupuesto_repo(db: Session = Depends(get_db)) -> PresupuestoRepository:
    return PresupuestoRepository(db)


@router.get("/", response_model=list[PresupuestoResponse])
def listar(
    current_user: dict = Depends(get_current_user),
    repo: PresupuestoRepository = Depends(get_presupuesto_repo),
):
    """Lista todos los presupuestos del usuario con su gasto real y % consumido."""
    return listar_presupuestos(current_user["user_id"], repo)


@router.post("/", response_model=PresupuestoResponse)
def crear_o_actualizar(
    data: PresupuestoCreate,
    current_user: dict = Depends(get_current_user),
    repo: PresupuestoRepository = Depends(get_presupuesto_repo),
):
    """Crea o actualiza el límite de presupuesto para una categoría."""
    if data.limite <= 0:
        raise HTTPException(status_code=400, detail="El límite debe ser mayor a 0.")

    p = repo.crear_o_actualizar(
        user_id=current_user["user_id"],
        categoria_id=data.categoria_id,
        limite=data.limite,
        mes=data.mes,
        anio=data.anio,
    )
    # Calcular gasto y estado para la respuesta
    gastado = repo.calcular_gasto_en_periodo(
        current_user["user_id"], p.categoria_id, p.mes, p.anio
    )
    pct = round((gastado / p.limite) * 100, 1) if p.limite > 0 else 0.0
    estado = "excedido" if pct >= 100 else "advertencia" if pct >= 75 else "ok"

    return PresupuestoResponse(
        id=p.id,
        categoria_id=p.categoria_id,
        categoria_nombre=p.categoria.nombre,
        limite=p.limite,
        mes=p.mes,
        anio=p.anio,
        gastado=round(gastado, 2),
        pct_usado=pct,
        estado=estado,
    )


@router.delete("/{presupuesto_id}")
def eliminar(
    presupuesto_id: int,
    current_user: dict = Depends(get_current_user),
    repo: PresupuestoRepository = Depends(get_presupuesto_repo),
):
    """Elimina un presupuesto del usuario."""
    ok = repo.eliminar(presupuesto_id, current_user["user_id"])
    if not ok:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado.")
    return {"ok": True}


@router.get("/alertas", response_model=list[AlertaPresupuesto])
def alertas(
    current_user: dict = Depends(get_current_user),
    repo: PresupuestoRepository = Depends(get_presupuesto_repo),
):
    """Devuelve solo los presupuestos en advertencia o excedidos (para el banner del dashboard)."""
    return obtener_alertas(current_user["user_id"], repo)
