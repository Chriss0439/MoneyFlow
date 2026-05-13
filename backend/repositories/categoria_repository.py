"""
repositories/categoria_repository.py
------------------------------------
Repositorio (El Bodeguero) para la tabla `categorias`.
Único lugar con consultas SQLAlchemy para las categorías.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Categoria


class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_todas(self) -> list[Categoria]:
        """Devuelve todas las categorías de la base de datos."""
        return self.db.query(Categoria).all()

    def nombre_existe(self, nombre: str) -> bool:
        """Verifica si una categoría con ese nombre ya existe."""
        return self.db.query(Categoria).filter(Categoria.nombre == nombre).first() is not None

    def crear(self, nombre: str, tipo: str) -> Categoria:
        """Inserta una nueva categoría en la BD."""
        nueva = Categoria(nombre=nombre, tipo=tipo)
        self.db.add(nueva)
        self.db.commit()
        self.db.refresh(nueva)
        return nueva
