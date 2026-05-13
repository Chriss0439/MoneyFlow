@echo off
title Iniciando MoneyFlow
echo ==========================================
echo    Iniciando MoneyFlow
echo ==========================================
echo.
echo Creando entorno virtual e instalando dependencias (puede tardar la primera vez)...

cd backend

:: Crea el entorno virtual si no existe
if not exist venv\ (
    python -m venv venv
)

:: Activa el entorno virtual
call venv\Scripts\activate

:: Instala las dependencias
pip install -r requirements.txt >nul 2>&1

echo.
echo   Backend API:  http://localhost:8000/docs
echo   Aplicacion:   http://localhost:8000
echo.
echo Para detener el servidor, cierra esta ventana o presiona Ctrl+C
echo.

:: Abre el navegador despues de 2 segundos (usando un ping local como delay)
start "" /B cmd /c "ping localhost -n 3 >nul && start http://localhost:8000"

:: Inicia Uvicorn
uvicorn main:app --reload --reload-dir . --reload-exclude "venv" --port 8000
