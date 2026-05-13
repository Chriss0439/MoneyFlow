"""
services/movimientos.py
-----------------------
Lógica de negocio para registrar y listar movimientos.
"""
from datetime import date
from schemas.movimientos import MovimientoCreate, MovimientoResponse
from repositories.movimiento_repository import MovimientoRepository
from sqlalchemy.orm import Session
from models import Categoria

class CategoriaNoExisteError(Exception):
    """Se lanza cuando se intenta asociar un movimiento a una categoría inexistente."""


def listar_movimientos_usuario(user_id: int, repo: MovimientoRepository, mes: int = None, anio: int = None, categoria_id: int = None) -> list[MovimientoResponse]:
    """Obtiene los movimientos del usuario y les inyecta el tipo de categoría para facilidad del frontend."""
    movimientos_orm = repo.obtener_por_usuario(user_id, mes, anio, categoria_id)
    
    resultados = []
    for mov in movimientos_orm:
        # Convertimos a Pydantic
        mov_response = MovimientoResponse.model_validate(mov)
        # Extraemos el tipo de categoría gracias a la relación de SQLAlchemy
        mov_response.tipo_categoria = mov.categoria.tipo if mov.categoria else None
        resultados.append(mov_response)
        
    return resultados


def registrar_movimiento(user_id: int, datos: MovimientoCreate, repo: MovimientoRepository, db: Session) -> MovimientoResponse:
    """Registra el gasto o ingreso asegurándose de que la categoría exista."""
    
    # 1. Validar que la categoría exista
    categoria = db.query(Categoria).filter(Categoria.id == datos.categoria_id).first()
    if not categoria:
        raise CategoriaNoExisteError("La categoría especificada no existe.")

    # 2. Asignar fecha de hoy si no viene en los datos
    fecha_final = datos.fecha if datos.fecha else date.today()

    # 3. Guardar en BD
    nuevo_movimiento = repo.crear(
        user_id=user_id,
        categoria_id=datos.categoria_id,
        monto=datos.monto,
        descripcion=datos.descripcion,
        fecha=fecha_final,
        es_apoyo_familiar=datos.es_apoyo_familiar
    )
    
    # 4. Formatear la respuesta
    response = MovimientoResponse.model_validate(nuevo_movimiento)
    response.tipo_categoria = categoria.tipo
    return response

def eliminar_movimiento(user_id: int, movimiento_id: int, repo: MovimientoRepository):
    """Verifica la eliminación del movimiento y lanza error si no existe."""
    exito = repo.borrar(movimiento_id, user_id)
    if not exito:
        raise Exception("Movimiento no encontrado o no autorizado para borrar.")
    return {"detail": "Movimiento eliminado con éxito"}
