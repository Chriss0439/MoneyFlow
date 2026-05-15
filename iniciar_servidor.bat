@echo off
title Iniciando MoneyFlow
echo ==========================================
echo    Iniciando MoneyFlow
echo ==========================================
echo.

:: Posicionarse siempre en la carpeta del .bat, sin importar desde donde se ejecute
cd /d "%~dp0backend"

:: Detectar Python (intenta primero "py", luego "python")
where py >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON=py
) else (
    where python >nul 2>&1
    if %errorlevel% == 0 (
        set PYTHON=python
    ) else (
        echo ERROR: Python no esta instalado o no esta en el PATH.
        echo Descargalo desde https://www.python.org/downloads/
        echo Asegurate de marcar "Add Python to PATH" durante la instalacion.
        pause
        exit /b 1
    )
)

:: Crear el entorno virtual si no existe
if not exist venv\ (
    echo Creando entorno virtual...
    %PYTHON% -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
)

:: Activar el entorno virtual
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ERROR: No se pudo activar el entorno virtual.
    pause
    exit /b 1
)

:: Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt >nul 2>&1

echo.
echo   Backend API:  http://localhost:8000/docs
echo   Aplicacion:   http://localhost:8000
echo.
echo Para detener el servidor, cierra esta ventana o presiona Ctrl+C
echo.

:: Abrir el navegador despues de un breve retraso
start "" /B cmd /c "ping localhost -n 3 >nul && start http://localhost:8000"

:: Iniciar Uvicorn usando la ruta explicita del entorno virtual
venv\Scripts\uvicorn main:app --reload --reload-dir . --reload-exclude "venv" --port 8000
