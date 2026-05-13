"""
models.py
---------
Definición de las tablas de la base de datos usando SQLAlchemy (ORM).
Esto reemplaza a los archivos .sql, permitiendo que Python cree y maneje las tablas.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, date

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # Relación: Un usuario tiene muchos movimientos
    movimientos = relationship("Movimiento", back_populates="user", cascade="all, delete-orphan")


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    tipo = Column(String, nullable=False)  # 'ingreso' o 'gasto'

    # Relación: Una categoría tiene muchos movimientos
    movimientos = relationship("Movimiento", back_populates="categoria")


class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    monto = Column(Float, nullable=False)
    descripcion = Column(String, nullable=True)
    fecha = Column(Date, default=date.today)
    es_apoyo_familiar = Column(Boolean, default=False)

    # Relaciones inversas
    user = relationship("User", back_populates="movimientos")
    categoria = relationship("Categoria", back_populates="movimientos")
