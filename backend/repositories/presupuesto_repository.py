"""
repositories/presupuesto_repository.py
---------------------------------------
Repositorio para la tabla `presupuestos`.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from models import Presupuesto, Movimiento, Categoria
from datetime import date


class PresupuestoRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_o_actualizar(self, user_id: int, categoria_id: int, limite: float,
                           mes: int = None, anio: int = None) -> Presupuesto:
        """
        Crea un presupuesto nuevo o actualiza el límite si ya existe uno
        para ese usuario + categoría + mes/año.
        """
        existente = self.db.query(Presupuesto).filter(
            Presupuesto.user_id == user_id,
            Presupuesto.categoria_id == categoria_id,
            Presupuesto.mes == mes,
            Presupuesto.anio == anio,
        ).first()

        if existente:
            existente.limite = limite
            self.db.commit()
            self.db.refresh(existente)
            return existente

        nuevo = Presupuesto(
            user_id=user_id,
            categoria_id=categoria_id,
            limite=limite,
            mes=mes,
            anio=anio,
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def obtener_por_usuario(self, user_id: int) -> list[Presupuesto]:
        """Lista todos los presupuestos del usuario con su categoría."""
        return (
            self.db.query(Presupuesto)
            .filter(Presupuesto.user_id == user_id)
            .join(Categoria)
            .order_by(Categoria.nombre)
            .all()
        )

    def eliminar(self, presupuesto_id: int, user_id: int) -> bool:
        """Elimina un presupuesto del usuario. Retorna True si tuvo éxito."""
        p = self.db.query(Presupuesto).filter(
            Presupuesto.id == presupuesto_id,
            Presupuesto.user_id == user_id,
        ).first()
        if p:
            self.db.delete(p)
            self.db.commit()
            return True
        return False

    def calcular_gasto_en_periodo(self, user_id: int, categoria_id: int,
                                  mes: int = None, anio: int = None) -> float:
        """
        Suma los gastos del usuario en una categoría para el período del presupuesto.

        SQL equivalente:
        SELECT SUM(m.monto) FROM movimientos m
        JOIN categorias c ON m.categoria_id = c.id
        WHERE m.user_id = ? AND m.categoria_id = ? AND c.tipo = 'gasto'
          [AND strftime('%m', m.fecha) = ?]  [AND strftime('%Y', m.fecha) = ?]
        """
        query = self.db.query(func.sum(Movimiento.monto)).join(Categoria).filter(
            Movimiento.user_id == user_id,
            Movimiento.categoria_id == categoria_id,
            Categoria.tipo == 'gasto',
        )
        if mes:
            query = query.filter(extract('month', Movimiento.fecha) == mes)
        if anio:
            query = query.filter(extract('year', Movimiento.fecha) == anio)

        resultado = query.scalar()
        return resultado or 0.0
