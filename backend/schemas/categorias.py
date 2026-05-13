"""
schemas/categorias.py
---------------------
Modelos (La Comanda) para el módulo de Categorías.
"""
from pydantic import BaseModel


class CategoriaBase(BaseModel):
    nombre: str
    tipo: str  # Debe ser 'ingreso' o 'gasto'


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        # Permite que Pydantic lea los datos directamente del modelo ORM de SQLAlchemy
        from_attributes = True
