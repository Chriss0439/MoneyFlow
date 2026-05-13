"""
schemas/auth.py
---------------
Modelos Pydantic para el módulo de autenticación.
Define la forma de los datos que entran y salen de la API.
"""
from pydantic import BaseModel, EmailStr


# ─── Requests (entrada) ────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    nombre: str
    correo: EmailStr
    password: str


class LoginRequest(BaseModel):
    correo: EmailStr
    password: str


# ─── Responses (salida) ────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    nombre: str


class UserResponse(BaseModel):
    """Datos del usuario autenticado (usado en /auth/me)."""
    user_id: int
    nombre: str
    correo: str
