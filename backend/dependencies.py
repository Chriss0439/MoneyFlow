"""
dependencies.py
---------------
Dependencias de FastAPI reutilizables entre todos los módulos.
Se inyectan con Depends() en cualquier ruta que lo necesite.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from security import decode_token
from database import get_db
from repositories.user_repository import UserRepository
from repositories.categoria_repository import CategoriaRepository
from repositories.movimiento_repository import MovimientoRepository

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """
    Dependencia de autenticación.
    Valida el JWT del header Authorization: Bearer <token>.
    Retorna el payload del token: {user_id, nombre, correo}.
    Uso:  current_user: dict = Depends(get_current_user)
    """
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    """
    Inyecta una instancia de UserRepository configurada con la sesión de DB actual.
    """
    return UserRepository(db)

def get_categoria_repo(db: Session = Depends(get_db)) -> CategoriaRepository:
    """
    Inyecta una instancia de CategoriaRepository configurada con la sesión de DB actual.
    """
    return CategoriaRepository(db)

def get_movimiento_repo(db: Session = Depends(get_db)) -> MovimientoRepository:
    """
    Inyecta una instancia de MovimientoRepository configurada con la sesión de DB actual.
    """
    return MovimientoRepository(db)


