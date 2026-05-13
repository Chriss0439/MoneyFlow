"""
routes/auth.py
--------------
Capa HTTP del módulo de autenticación.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from services.auth import (
    CorreoDuplicadoError,
    CredencialesInvalidasError,
    autenticar_usuario,
    registrar_usuario,
)
from dependencies import get_current_user, get_user_repo
from repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, user_repo: UserRepository = Depends(get_user_repo)):
    """Registra un nuevo usuario y retorna un JWT de sesión."""
    try:
        return registrar_usuario(body.nombre, body.correo, body.password, user_repo)
    except CorreoDuplicadoError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, user_repo: UserRepository = Depends(get_user_repo)):
    """Autentica un usuario y retorna un JWT."""
    try:
        return autenticar_usuario(body.correo, body.password, user_repo)
    except CredencialesInvalidasError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    """Retorna los datos del usuario autenticado."""
    return UserResponse(
        user_id=current_user["user_id"],
        nombre=current_user["nombre"],
        correo=current_user["correo"],
    )
