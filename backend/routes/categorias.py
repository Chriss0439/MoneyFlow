"""
routes/categorias.py
--------------------
Capa HTTP (El Mesero) para Categorías.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from schemas.categorias import CategoriaCreate, CategoriaResponse
from services.categorias import listar_categorias, crear_categoria, CategoriaDuplicadaError, TipoCategoriaInvalidoError
from dependencies import get_current_user, get_categoria_repo
from repositories.categoria_repository import CategoriaRepository

# Note: Todas las rutas de categorías requieren que el usuario esté autenticado.
router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"],
    dependencies=[Depends(get_current_user)] # Protege todo el router
)


@router.get("/", response_model=List[CategoriaResponse])
def get_categorias(repo: CategoriaRepository = Depends(get_categoria_repo)):
    """Retorna la lista de todas las categorías disponibles en el sistema."""
    return listar_categorias(repo)


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def create_categoria(body: CategoriaCreate, repo: CategoriaRepository = Depends(get_categoria_repo)):
    """Crea una nueva categoría (gasto o ingreso)."""
    try:
        return crear_categoria(body.nombre, body.tipo, repo)
    except TipoCategoriaInvalidoError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except CategoriaDuplicadaError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
