"""
repositories/user_repository.py
--------------------------------
Repositorio de la tabla `users` usando SQLAlchemy.
Maneja las operaciones de base de datos ocultando la complejidad del ORM al resto de la app.
"""
from sqlalchemy.orm import Session
from models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_correo(self, correo: str) -> User | None:
        """Busca un usuario por su correo electrónico."""
        return self.db.query(User).filter(User.correo == correo).first()

    def buscar_por_id(self, user_id: int) -> User | None:
        """Busca un usuario por su ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def correo_existe(self, correo: str) -> bool:
        """Retorna True si el correo ya está registrado."""
        return self.buscar_por_correo(correo) is not None

    def crear(self, nombre: str, correo: str, password_hash: str) -> User:
        """Crea un usuario nuevo y lo guarda en la BD."""
        nuevo_usuario = User(
            nombre=nombre,
            correo=correo,
            password_hash=password_hash
        )
        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)
        return nuevo_usuario
