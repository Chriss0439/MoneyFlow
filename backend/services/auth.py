"""
services/auth.py
----------------
Lógica de negocio del módulo de autenticación.
"""
import bcrypt

from security import create_access_token
from schemas.auth import TokenResponse
from repositories.user_repository import UserRepository


# ─── Helpers de contraseña ─────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


# ─── Excepciones del dominio ───────────────────────────────────────────────────

class CorreoDuplicadoError(Exception):
    """Se lanza cuando el correo ya está registrado."""


class CredencialesInvalidasError(Exception):
    """Se lanza cuando correo o contraseña no coinciden."""


# ─── Lógica de negocio ─────────────────────────────────────────────────────────

def registrar_usuario(nombre: str, correo: str, password: str, user_repo: UserRepository) -> TokenResponse:
    """Registra un nuevo usuario usando SQLAlchemy."""
    if user_repo.correo_existe(correo):
        raise CorreoDuplicadoError(f"El correo '{correo}' ya está registrado.")

    hashed = hash_password(password)
    
    nuevo_usuario = user_repo.crear(nombre, correo, hashed)

    token = create_access_token({"user_id": nuevo_usuario.id, "nombre": nombre, "correo": correo})
    return TokenResponse(access_token=token, user_id=nuevo_usuario.id, nombre=nombre)


def autenticar_usuario(correo: str, password: str, user_repo: UserRepository) -> TokenResponse:
    """Autentica un usuario existente usando SQLAlchemy."""
    user = user_repo.buscar_por_correo(correo)

    if user is None or not verify_password(password, user.password_hash):
        raise CredencialesInvalidasError("Correo o contraseña incorrectos.")

    token = create_access_token({
        "user_id": user.id,
        "nombre": user.nombre,
        "correo": user.correo,
    })
    return TokenResponse(access_token=token, user_id=user.id, nombre=user.nombre)
