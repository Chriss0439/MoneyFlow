# MoneyFlow 💸

Una aplicación web mobile-first para la gestión de finanzas personales. Permite registrar ingresos y gastos, gestionar categorías, definir presupuestos con alertas automáticas y visualizar reportes interactivos junto con métricas de independencia financiera.

## 🛠️ Tecnologías
*   **Backend:** Python 3 + FastAPI
*   **Base de Datos:** SQLite (Local)
*   **Frontend:** HTML5, CSS3, Vanilla JS
*   **Gráficas:** Chart.js

---

## 🚀 Cómo ejecutar el proyecto localmente

Este proyecto está diseñado para funcionar inmediatamente después de descargarse, ya que utiliza SQLite como base de datos y FastAPI sirve tanto la API como el Frontend.

### Opción 1: Ejecución Automática (Mac / Windows)
La forma más fácil de probar el proyecto es mediante los scripts incluidos, los cuales configurarán el entorno, instalarán las dependencias necesarias y abrirán tu navegador.

**Para Mac / Linux:**
1. Abre tu terminal en la carpeta del proyecto.
2. Ejecuta el archivo Bash:
   ```bash
   bash iniciar_servidor.command
   ```
*(Alternativamente, puedes darle permisos de ejecución `chmod +x iniciar_servidor.command` y hacerle doble clic).*

**Para Windows:**
1. Simplemente haz **doble clic** en el archivo `iniciar_servidor.bat`.
*(Opcional: Si el sistema te pregunta, dale permisos para ejecutarse).*

---

### Opción 2: Instalación Manual (Paso a paso)

**1. Crea un entorno virtual (Recomendado):**
```bash
cd backend
python -m venv venv
```

**2. Activa el entorno virtual:**
*   **Windows:** `venv\Scripts\activate`
*   **Mac/Linux:** `source venv/bin/activate`

**3. Instala las dependencias:**
```bash
pip install -r requirements.txt
```

**4. Levanta el servidor:**
```bash
uvicorn main:app --reload --port 8000
```

**5. Abre la aplicación:**
Ingresa a [http://localhost:8000](http://localhost:8000) en tu navegador Chrome (se recomienda usar la herramienta de inspección F12 en modo "Teléfono Móvil" para la mejor experiencia).

---

## 💾 Sobre la Base de Datos
La primera vez que levantes el servidor, la aplicación detectará que no tienes base de datos y automáticamente creará el archivo `moneyflow.db` con todas las tablas necesarias (`users`, `categorias`, `movimientos` y `presupuestos`).

Si deseas que la base de datos tenga las **categorías predeterminadas** ya listas para usar:
1. Con el entorno virtual activado, corre el script de poblamiento:
   ```bash
   python seed_data.py
   ```
