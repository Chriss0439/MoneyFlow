"""
services/categorias.py
----------------------
Lógica de negocio (El Chef) para las Categorías.
"""
from schemas.categorias import CategoriaResponse
from repositories.categoria_repository import CategoriaRepository

class CategoriaDuplicadaError(Exception):
    """Se lanza cuando se intenta crear una categoría que ya existe."""

class TipoCategoriaInvalidoError(Exception):
    """Se lanza cuando el tipo no es 'ingreso' ni 'gasto'."""


def listar_categorias(repo: CategoriaRepository) -> list[CategoriaResponse]:
    """Obtiene el listado de todas las categorías disponibles."""
    categorias_orm = repo.obtener_todas()
    # Pydantic (gracias a from_attributes=True) se encarga de convertir esto al salir de las rutas
    return categorias_orm


def crear_categoria(nombre: str, tipo: str, repo: CategoriaRepository) -> CategoriaResponse:
    """Crea una nueva categoría validando el tipo y que no esté duplicada."""
    tipo = tipo.lower().strip()
    nombre = nombre.strip()
    
    if tipo not in ["ingreso", "gasto"]:
        raise TipoCategoriaInvalidoError("El tipo de categoría debe ser 'ingreso' o 'gasto'.")
        
    if repo.nombre_existe(nombre):
        raise CategoriaDuplicadaError(f"La categoría '{nombre}' ya existe.")
        
    nueva_cat = repo.crear(nombre, tipo)
    return nueva_cat
