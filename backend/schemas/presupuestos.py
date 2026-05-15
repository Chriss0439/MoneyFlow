"""
schemas/presupuestos.py
-----------------------
Modelos Pydantic para el módulo de Presupuestos.
"""
from pydantic import BaseModel
from typing import Optional


class PresupuestoCreate(BaseModel):
    categoria_id: int
    limite: float
    mes: Optional[int] = None    # Si None, aplica a todos los meses
    anio: Optional[int] = None   # Si None, aplica a todos los años


class PresupuestoResponse(BaseModel):
    id: int
    categoria_id: int
    categoria_nombre: str
    limite: float
    mes: Optional[int]
    anio: Optional[int]
    gastado: float        # Gasto real acumulado en el período
    pct_usado: float      # % del límite que ya se usó
    estado: str           # "ok" | "advertencia" | "excedido"

    class Config:
        from_attributes = True


class AlertaPresupuesto(BaseModel):
    presupuesto_id: int
    categoria_nombre: str
    limite: float
    gastado: float
    pct_usado: float
    estado: str           # "advertencia" (>=75%) | "excedido" (>=100%)
