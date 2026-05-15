# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from database import init_db
from routes.auth import router as auth_router
from routes.categorias import router as categorias_router
from routes.movimientos import router as movimientos_router
from routes.dashboard import router as dashboard_router
from routes.reportes import router as reportes_router
from routes.presupuestos import router as presupuestos_router

# ─── Inicializar la app ─────────────────────────────────────────────────────────
app = FastAPI(
    title="MoneyFlow API",
    description="API de gestión financiera para estudiantes universitarias.",
    version="1.0.0",
)

# ─── CORS: permite que el frontend (HTML/JS) llame a la API ────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # En producción: especificar el dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Registrar routers ─────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(categorias_router)
app.include_router(movimientos_router)
app.include_router(dashboard_router)
app.include_router(reportes_router)
app.include_router(presupuestos_router)

# app.include_router(categorias_router)
# app.include_router(reportes_router)


# ─── Evento de inicio: inicializa la BD si está vacía ─────────────────────────
@app.on_event("startup")
def on_startup():
    init_db()


# ─── Servir el Frontend (HTML/CSS/JS) ────────────────────────────────────────
# Calcula la ruta absoluta a la carpeta 'frontend' que está un nivel arriba del backend
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")

@app.get("/", tags=["Frontend"], include_in_schema=False)
def serve_frontend():
    """Ruta raíz: devuelve la app web (index.html)."""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Montamos los archivos estáticos (CSS, JS, imágenes) bajo /static
# Esto se hace AL FINAL para que no intercepte las rutas de la API
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
