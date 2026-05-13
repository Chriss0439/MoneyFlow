#!/bin/bash
# Este script levanta el servidor de MoneyFlow (Backend + Frontend unificados)

# Obtiene la ruta exacta de la carpeta donde está este archivo
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Entra a la carpeta del backend
cd "$DIR/backend"

echo "=========================================="
echo "   Iniciando MoneyFlow"
echo "=========================================="
echo "  Backend API:  http://localhost:8000/docs"
echo "  Aplicación:   http://localhost:8000"
echo ""
echo "Para detener el servidor, cierra esta ventana o presiona Ctrl+C"
echo ""

# Abre el navegador después de 2 segundos (le da tiempo al servidor de arrancar)
sleep 2 && open "http://localhost:8000" &

# Activa el entorno virtual e inicia Uvicorn
source venv/bin/activate
uvicorn main:app --reload --reload-dir . --reload-exclude "venv" --port 8000
