import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

# ─── Configuración del token JWT ───────────────────────────────────────────────
# En producción esto vendría de una variable de entorno
SECRET_KEY = os.getenv("MONEYFLOW_SECRET", "moneyflow-dev-secret-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 horas (una jornada de uso)


def create_access_token(data: dict) -> str:
    """Genera un JWT firmado con los datos del usuario y tiempo de expiración."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    """Decodifica y valida un JWT. Retorna el payload o None si es inválido."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
