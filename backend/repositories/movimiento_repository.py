"""
repositories/movimiento_repository.py
-------------------------------------
Repositorio para la tabla `movimientos`.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Movimiento, Categoria
from datetime import date

class MovimientoRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, user_id: int, categoria_id: int, monto: float, descripcion: str, fecha: date, es_apoyo_familiar: bool) -> Movimiento:
        """Crea un nuevo movimiento asociado a un usuario y una categoría."""
        nuevo = Movimiento(
            user_id=user_id,
            categoria_id=categoria_id,
            monto=monto,
            descripcion=descripcion,
            fecha=fecha,
            es_apoyo_familiar=es_apoyo_familiar
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def obtener_por_usuario(self, user_id: int, mes: int = None, anio: int = None, categoria_id: int = None) -> list[Movimiento]:
        """Obtiene todos los movimientos de un usuario, opcionalmente filtrados por mes, año o categoría."""
        query = self.db.query(Movimiento).filter(Movimiento.user_id == user_id)
        
        # Filtrado de fechas extraídas en SQLite
        from sqlalchemy import extract
        if anio:
            query = query.filter(extract('year', Movimiento.fecha) == anio)
        if mes:
            query = query.filter(extract('month', Movimiento.fecha) == mes)
            
        if categoria_id:
            query = query.filter(Movimiento.categoria_id == categoria_id)
            
        return query.order_by(Movimiento.fecha.desc(), Movimiento.id.desc()).all()

    def borrar(self, movimiento_id: int, user_id: int) -> bool:
        """Busca un movimiento del usuario y lo elimina. Retorna True si tuvo éxito."""
        movimiento = self.db.query(Movimiento).filter(
            Movimiento.id == movimiento_id, 
            Movimiento.user_id == user_id
        ).first()
        
        if movimiento:
            self.db.delete(movimiento)
            self.db.commit()
            return True
        return False

    def obtener_totales_por_usuario(self, user_id: int) -> dict:
        """
        Ejecuta un JOIN entre Movimientos y Categorías para sumarizar los montos.
        Retorna: {"ingreso": 1500.0, "gasto": 50.0}
        """
        # SQL Equivalente: 
        # SELECT c.tipo, SUM(m.monto) FROM movimientos m 
        # JOIN categorias c ON m.categoria_id = c.id 
        # WHERE m.user_id = ? GROUP BY c.tipo
        resultados = self.db.query(
            Categoria.tipo, 
            func.sum(Movimiento.monto)
        ).join(Movimiento).filter(Movimiento.user_id == user_id).group_by(Categoria.tipo).all()

        totales = {"ingreso": 0.0, "gasto": 0.0}
        for tipo, total in resultados:
            totales[tipo] = total or 0.0
            
        return totales

    def obtener_gastos_por_categoria(self, user_id: int) -> list[dict]:
        """
        Agrupa los gastos del usuario por nombre de categoría para la gráfica.
        SELECT c.nombre, SUM(m.monto) FROM movimientos m JOIN categorias c ON m.categoria_id = c.id
        WHERE m.user_id = ? AND c.tipo = 'gasto' GROUP BY c.nombre
        """
        resultados = self.db.query(
            Categoria.nombre,
            func.sum(Movimiento.monto).label('total')
        ).join(Movimiento).filter(
            Movimiento.user_id == user_id,
            Categoria.tipo == 'gasto'
        ).group_by(Categoria.nombre).all()
        
        return [{"categoria": r.nombre, "total": r.total or 0.0} for r in resultados]


