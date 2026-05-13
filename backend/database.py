"""
database.py
-----------
Configuración de la conexión a la base de datos usando SQLAlchemy.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Categoria

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "moneyflow.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# check_same_thread=False es necesario para SQLite en FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Crea las tablas si no existen e inserta datos iniciales."""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    # Sembrar categorías por defecto si no existen
    if not db.query(Categoria).first():
        categorias_iniciales = [
            Categoria(nombre='Apoyo Familiar', tipo='ingreso'),
            Categoria(nombre='Freelance/Emprendimiento', tipo='ingreso'),
            Categoria(nombre='Fotocopias y Libros', tipo='gasto'),
            Categoria(nombre='Alimentación/Cafetería', tipo='gasto'),
            Categoria(nombre='Transporte', tipo='gasto')
        ]
        db.add_all(categorias_iniciales)
        db.commit()
    db.close()

def get_db():
    """Dependencia para obtener una sesión de la base de datos por cada request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
