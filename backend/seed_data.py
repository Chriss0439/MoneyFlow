import sys
import os
from datetime import date, timedelta
import random

# Asegurar que las importaciones funcionen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import User, Categoria, Movimiento
# Sin dependencias extra

def seed_database():
    db = SessionLocal()
    
    try:
        # 1. Crear un usuario de prueba si no hay ninguno
        usuario = db.query(User).first()
        if not usuario:
            print("Creando usuario de prueba...")
            usuario = User(
                nombre="Christian Marquez",
                email="christian@correo.edu",
                hashed_password="dummy_hash_for_testing"
            )
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
        
        user_id = usuario.id
        print(f"Usando usuario ID: {user_id} ({usuario.nombre})")

        # 2. Crear categorías del Mockup
        categorias_mockup = [
            {"nombre": "Salario", "tipo": "ingreso"},
            {"nombre": "Freelance", "tipo": "ingreso"},
            {"nombre": "Inversiones", "tipo": "ingreso"},
            {"nombre": "Alimentos", "tipo": "gasto"},
            {"nombre": "Transporte", "tipo": "gasto"},
            {"nombre": "Entretenimiento", "tipo": "gasto"},
            {"nombre": "Educación", "tipo": "gasto"},
            {"nombre": "Salud", "tipo": "gasto"},
            {"nombre": "Ropa", "tipo": "gasto"}
        ]
        
        cat_ids = {"ingreso": [], "gasto": []}
        
        print("Verificando/Creando categorías...")
        for c in categorias_mockup:
            cat_db = db.query(Categoria).filter_by(nombre=c["nombre"]).first()
            if not cat_db:
                cat_db = Categoria(nombre=c["nombre"], tipo=c["tipo"])
                db.add(cat_db)
                db.commit()
                db.refresh(cat_db)
            cat_ids[c["tipo"]].append(cat_db.id)
            
        # 3. Generar movimientos aleatorios realistas
        print("Generando movimientos...")
        
        # Generar fechas de los últimos 60 días
        hoy = date.today()
        
        # Gastos descriptivos
        descripciones_gasto = {
            "Alimentos": ["Supermercado La Torre", "Walmart", "McDonalds", "Cena con amigos", "Café en la U", "Uber Eats"],
            "Transporte": ["Gasolina Shell", "Uber", "Bus", "Mantenimiento auto", "Parqueo"],
            "Entretenimiento": ["Cine", "Suscripción Netflix", "Spotify", "Videojuegos", "Salida fin de semana"],
            "Educación": ["Libros texto", "Cuota Universidad", "Curso en línea", "Materiales papelería"],
            "Salud": ["Farmacia", "Consulta médica", "Vitaminas"],
            "Ropa": ["Zapatos nuevos", "Camisa Zara", "Pantalón"]
        }
        
        movimientos_creados = 0
        
        # Agregar 15 gastos
        for _ in range(15):
            dias_atras = random.randint(0, 60)
            fecha = hoy - timedelta(days=dias_atras)
            
            # Seleccionar una categoría de gasto al azar
            cat_db = db.query(Categoria).filter(Categoria.id.in_(cat_ids["gasto"])).order_by(func.random()).first()
            
            if cat_db and cat_db.nombre in descripciones_gasto:
                desc = random.choice(descripciones_gasto[cat_db.nombre])
                # Monto entre Q50 y Q800
                monto = round(random.uniform(50, 800), 2)
                
                mov = Movimiento(
                    user_id=user_id,
                    categoria_id=cat_db.id,
                    monto=monto,
                    descripcion=desc,
                    fecha=fecha,
                    es_apoyo_familiar=False
                )
                db.add(mov)
                movimientos_creados += 1
                
        # Agregar 4 ingresos fijos (salarios/freelance de los ultimos 2 meses)
        ingresos_data = [
            ("Salario", 4500.00, hoy - timedelta(days=5)),
            ("Freelance", 1200.00, hoy - timedelta(days=15)),
            ("Salario", 4500.00, hoy - timedelta(days=35)),
            ("Inversiones", 350.00, hoy - timedelta(days=45))
        ]
        
        for nom, monto, fecha in ingresos_data:
            cat_db = db.query(Categoria).filter_by(nombre=nom).first()
            if cat_db:
                mov = Movimiento(
                    user_id=user_id,
                    categoria_id=cat_db.id,
                    monto=monto,
                    descripcion=nom + " Mensual",
                    fecha=fecha,
                    es_apoyo_familiar=False
                )
                db.add(mov)
                movimientos_creados += 1

        db.commit()
        print(f"¡Éxito! Se inyectaron {movimientos_creados} movimientos de prueba en la base de datos.")

    except Exception as e:
        print(f"Error al poblar base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    from sqlalchemy.sql.expression import func
    seed_database()
