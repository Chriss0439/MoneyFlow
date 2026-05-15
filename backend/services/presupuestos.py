"""
services/presupuestos.py
------------------------
Lógica de negocio para presupuestos y generación de alertas.
"""
from repositories.presupuesto_repository import PresupuestoRepository
from schemas.presupuestos import PresupuestoResponse, AlertaPresupuesto


def _calcular_estado(pct: float) -> str:
    """Devuelve el estado del presupuesto según el % consumido."""
    if pct >= 100:
        return "excedido"
    if pct >= 75:
        return "advertencia"
    return "ok"


def listar_presupuestos(user_id: int, repo: PresupuestoRepository) -> list[PresupuestoResponse]:
    """
    Devuelve todos los presupuestos del usuario enriquecidos con
    el gasto real acumulado y el % utilizado.
    """
    presupuestos = repo.obtener_por_usuario(user_id)
    resultado = []

    for p in presupuestos:
        gastado = repo.calcular_gasto_en_periodo(user_id, p.categoria_id, p.mes, p.anio)
        pct = round((gastado / p.limite) * 100, 1) if p.limite > 0 else 0.0

        resultado.append(PresupuestoResponse(
            id=p.id,
            categoria_id=p.categoria_id,
            categoria_nombre=p.categoria.nombre,
            limite=p.limite,
            mes=p.mes,
            anio=p.anio,
            gastado=round(gastado, 2),
            pct_usado=pct,
            estado=_calcular_estado(pct),
        ))

    return resultado


def obtener_alertas(user_id: int, repo: PresupuestoRepository) -> list[AlertaPresupuesto]:
    """
    Devuelve solo los presupuestos en estado 'advertencia' o 'excedido'.
    Se usa para mostrar el banner de alertas en el dashboard.
    """
    todos = listar_presupuestos(user_id, repo)
    return [
        AlertaPresupuesto(
            presupuesto_id=p.id,
            categoria_nombre=p.categoria_nombre,
            limite=p.limite,
            gastado=p.gastado,
            pct_usado=p.pct_usado,
            estado=p.estado,
        )
        for p in todos
        if p.estado in ("advertencia", "excedido")
    ]
