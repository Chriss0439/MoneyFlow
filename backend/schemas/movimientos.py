"""
schemas/movimientos.py
----------------------
Modelos para el módulo de Movimientos (Ingresos y Gastos).
"""
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class MovimientoBase(BaseModel):
    categoria_id: int
    monto: float = Field(gt=0, description="El monto debe ser mayor a cero")
    descripcion: Optional[str] = None
    fecha: Optional[date] = None
    es_apoyo_familiar: bool = False

class MovimientoCreate(MovimientoBase):
    pass

class MovimientoResponse(MovimientoBase):
    id: int
    user_id: int
    
    # Campo extra que agregaremos desde el backend para saber el tipo al leer
    tipo_categoria: Optional[str] = None 

    class Config:
        from_attributes = True
