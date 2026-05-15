# Documentación Técnica y Arquitectura — MoneyFlow 💸

Este documento describe a detalle la arquitectura del software, los patrones de diseño aplicados, el esquema de la base de datos y la organización de los módulos del proyecto MoneyFlow.

---

## 1. Arquitectura General del Sistema

MoneyFlow está diseñado bajo el patrón **Cliente-Servidor** utilizando una arquitectura de **Single Page Application (SPA)** acoplada a una **API REST**.

```mermaid
graph TD
    subgraph Frontend [Capa de Presentación / Cliente]
        UI[UI HTML/CSS/JS]
        Router[Router SPA app.js]
        Client[Cliente HTTP api.js]
    end

    subgraph Backend [Capa de Lógica / Servidor FastAPI]
        API[Rutas HTTP endpoints]
        Services[Servicios Lógica de Negocio]
        Repos[Repositorios Acceso a Datos]
    end

    subgraph Database [Capa de Persistencia]
        SQLite[(Base de Datos SQLite)]
    end

    UI -->|Eventos| Router
    Router -->|Llamadas asíncronas| Client
    Client -->|Peticiones HTTP/JSON| API
    API -->|Validación & Inyección| Services
    Services -->|Reglas de Negocio| Repos
    Repos -->|SQLAlchemy ORM| SQLite
```

---

## 2. Modelo de Datos (Diagrama Entidad-Relación)

La base de datos utiliza **SQLite** y es administrada a través del ORM SQLAlchemy. Se compone de 4 tablas fuertemente tipadas y relacionadas entre sí.

```mermaid
erDiagram
    USERS ||--o{ MOVIMIENTOS : registra
    USERS ||--o{ PRESUPUESTOS : define
    CATEGORIAS ||--o{ MOVIMIENTOS : clasifica
    CATEGORIAS ||--o{ PRESUPUESTOS : limita

    USERS {
        int id PK
        string nombre
        string correo UK
        string password_hash
        datetime fecha_registro
    }

    CATEGORIAS {
        int id PK
        string nombre UK
        string tipo "ingreso o gasto"
    }

    MOVIMIENTOS {
        int id PK
        int user_id FK
        int categoria_id FK
        float monto
        string descripcion
        date fecha
        boolean es_apoyo_familiar
    }

    PRESUPUESTOS {
        int id PK
        int user_id FK
        int categoria_id FK
        float limite
        int mes "nullable"
        int anio "nullable"
    }
```

---

## 3. Desglose del Backend (Python / FastAPI)

El backend sigue una arquitectura limpia en capas para separar responsabilidades. Está construido con **FastAPI**.

### 3.1. Arquitectura de Capas
* **Capa de Enrutamiento (`routes/`):** Recibe las peticiones HTTP, valida los parámetros (usando esquemas de Pydantic) y delega el trabajo. No contiene lógica de negocio.
* **Capa de Servicios (`services/`):** Contiene la "Lógica de Negocio". Aquí se procesan reglas como (Hashear contraseñas, armar las estadísticas matemáticas para el dashboard, emitir JWTs).
* **Capa de Repositorios (`repositories/`):** Aísla la base de datos del resto de la aplicación. Aquí se ejecutan directamente las consultas ORM de SQLAlchemy.
* **Capa de Modelos y Esquemas (`models.py`, `schemas/`):** Definen las estructuras de las tablas SQL y los validadores de JSON entrantes/salientes respectivamente.

### 3.2. Módulos Principales
1. **Autenticación (`auth`):**
   * Emplea hashing `bcrypt` para las contraseñas.
   * Genera y valida tokens `JWT` (JSON Web Tokens) para mantener la sesión abierta de manera segura sin estado (stateless).
2. **Dashboard (`dashboard`):**
   * Agrega matemáticamente los datos del usuario para calcular saldo actual (ingresos − gastos).
   * Calcula métricas de **independencia financiera**: desglose de ingresos propios vs. apoyo familiar usando el campo `es_apoyo_familiar` de cada movimiento, retornando montos y porcentajes listos para graficar.
3. **Movimientos (`movimientos`):**
   * Núcleo del sistema. Implementa el CRUD (Crear, Leer, Eliminar) para el flujo de dinero, incluyendo el filtrado avanzado por fecha o categoría.
4. **Reportes (`reportes`):**
   * Realiza agrupaciones (GROUP BY) en base de datos para sumar el total gastado en cada categoría y alimentar los gráficos de Chart.js.
5. **Presupuestos (`presupuestos`):**
   * Permite al usuario definir límites de gasto mensuales por categoría (opcionalmente acotados a un mes y año específicos).
   * Calcula en tiempo real el gasto acumulado frente al límite y determina el estado: `ok` (< 75%), `advertencia` (≥ 75%) o `excedido` (≥ 100%).
   * Expone el endpoint `GET /presupuestos/alertas` usado por el dashboard para mostrar el banner de alertas automáticamente al iniciar sesión.

---

## 4. Desglose del Frontend (Vanilla JS)

Se omitió el uso de frameworks complejos en favor de un enfoque ligero basado en "Vanilla JS", logrando un diseño "Mobile First" hiper rápido y de bajo costo de mantenimiento.

### 4.1. Estructura de Control
* **`index.html`:** Contenedor maestro. Posee múltiples etiquetas `<section class="view">` que representan cada pantalla del sistema.
* **`app.js` (El Router):** Se encarga de cambiar entre vistas modificando la clase `.active`. Además, controla la "Barra de Navegación Global" (Navbar) en función de si el usuario está en una pantalla principal o en un formulario. Posee el motor global de Notificaciones (`showToast`).
* **`api.js` (El Proxy de Red):** Centraliza todas las peticiones `fetch` hacia el backend, inyectando automáticamente el `JWT Token` de seguridad en los "Headers" de cada petición. Si detecta un "401 Unauthorized", desconecta al usuario de forma proactiva.

### 4.2. Controladores de Dominio (`controllers/`)
Cada vista tiene un archivo JS que asocia los eventos (`addEventListener`) a la interfaz:
* `auth.js`: Recolecta el form, llama a `api.login()` o `api.register()` y guarda el token en `localStorage`.
* `dashboard.js`: Lee los resúmenes, pinta las tarjetas de balance e independencia financiera (barras de % apoyo familiar vs. ingresos propios) y carga el historial de movimientos.
* `movimientos.js`: Dinamiza el `select` de categorías basado en si seleccionaste un gasto o un ingreso.
* `categorias.js`: Lista visualmente las fuentes de ingreso y tipos de gastos.
* `presupuestos.js`: Gestiona el CRUD de presupuestos, renderiza las barras de progreso con estado de color (verde/amarillo/rojo) y actualiza el banner de alertas del dashboard.

---

## 5. Diagramas de Secuencia:

### 5.1 Flujo de Inicio de Sesión

A continuación se grafica el ciclo de vida completo del inicio de sesión, incluyendo la validación de credenciales y la emisión del JWT.

```mermaid
sequenceDiagram
    actor Usuario
    participant UI as Frontend (UI/JS)
    participant API as Backend (FastAPI)
    participant Repo as Base de Datos (SQLite)

    Usuario->>UI: Ingresa correo y contraseña, clic "Entrar"
    UI->>API: POST /auth/login (correo, password)

    API->>Repo: SELECT * FROM users WHERE correo = ?
    Repo-->>API: Devuelve registro del usuario

    API->>API: bcrypt.verify(password, password_hash)

    alt Credenciales válidas
        API->>API: Genera JWT (expira en 7 días)
        API-->>UI: 200 OK (access_token)
        UI->>UI: localStorage.setItem("moneyflow_token", token)
        UI->>UI: showView("view-dashboard")
        UI->>Usuario: Muestra el dashboard
    else Credenciales inválidas
        API-->>UI: 401 Unauthorized
        UI->>Usuario: Muestra Toast de error
    end
```

### 5.2 Flujo de Registro de un Usuario

A continuación se grafica el ciclo de vida completo del registro, incluyendo la validación de correo único y el hash de contraseña.

```mermaid
sequenceDiagram
    actor Usuario
    participant UI as Frontend (UI/JS)
    participant API as Backend (FastAPI)
    participant Repo as Base de Datos (SQLite)

    Usuario->>UI: Llena nombre, correo y contraseña, clic "Comenzar"
    UI->>API: POST /auth/register (nombre, correo, password)

    API->>Repo: SELECT * FROM users WHERE correo = ?
    Repo-->>API: Resultado de búsqueda

    alt Correo ya registrado
        API-->>UI: 400 Bad Request ("El correo ya está registrado")
        UI->>Usuario: Muestra Toast de error
    else Correo disponible
        API->>API: bcrypt.hash(password) → password_hash
        API->>Repo: INSERT INTO users (nombre, correo, password_hash)
        Repo-->>API: Row insertado correctamente
        API->>API: Genera JWT para el nuevo usuario
        API-->>UI: 201 Created (access_token)
        UI->>UI: localStorage.setItem("moneyflow_token", token)
        UI->>UI: showView("view-dashboard")
        UI->>Usuario: Muestra el dashboard
    end
```

### 5.3 Flujo de Creación de un Gasto

A continuación se grafica el ciclo de vida completo de un evento común: el usuario registrando la compra de un "Uber".

```mermaid
sequenceDiagram
    actor Usuario
    participant UI as Frontend (UI/JS)
    participant API as Backend (FastAPI)
    participant Repo as Base de Datos (SQLite)

    Usuario->>UI: Clic en botón "Gasto"
    UI->>API: GET /categorias/
    API-->>UI: Devuelve lista de categorías
    UI->>Usuario: Muestra formulario

    Usuario->>UI: Llena monto, elige "Transporte" y clic Guardar
    UI->>API: POST /movimientos/ (Header: Bearer Token)
    
    API->>API: Valida Token JWT
    API->>API: Valida JSON entrante (Pydantic)
    
    API->>Repo: session.add(NuevoMovimiento)
    API->>Repo: session.commit()
    Repo-->>API: Row insertado correctamente
    
    API-->>UI: 201 Created (JSON del Movimiento)
    UI->>UI: Muestra notificación Toast (Verde)
    UI->>UI: Llama a showView('view-dashboard')
    UI->>Usuario: Muestra el dashboard actualizado
```

### 5.4 Flujo de Visualización del Dashboard

```mermaid
sequenceDiagram
    participant UI as Frontend (dashboard.js)
    participant API as Backend (reportes/dashboard)
    participant Repo as Base de Datos (SQLite)

    UI->>API: GET /reportes/gastos-por-categoria
    Note right of API: El Header incluye el Bearer Token
    
    API->>Repo: SELECT SUM(monto), categoria GROUP BY categoria
    Repo-->>API: Datos agrupados
    
    API->>API: Formatea datos para Chart.js
    API-->>UI: 200 OK (JSON con etiquetas y valores)
    
    UI->>UI: Inicializa Canvas (Chart.js)
    UI->>UI: Renderiza Gráfico de Torta/Barras
```

### 5.5 Flujo de Visualización de Reportes

```mermaid
sequenceDiagram
    actor Usuario
    participant UI as Frontend (reportes.js)
    participant API as Backend (reportes/movimientos)
    participant Repo as Base de Datos (SQLite)

    Usuario->>UI: Clic en Reportes
    UI->>UI: Limpia la tabla y el lienzo del gráfico
    
    UI->>API: GET /reportes/movimientos (Fecha: Enero)
    Note right of API: Header: Bearer Token
    
    API->>Repo: SELECT * FROM movimientos WHERE fecha >= ... ORDER BY fecha DESC
    Repo-->>API: Lista de 15 movimientos
    
    API->>API: Calcula Totales (Ingresos/Gastos)
    API-->>UI: 200 OK (Data + Totales)
    
    UI->>UI: Itera y dibuja filas en la tabla HTML
    UI->>UI: Inicializa Chart.js (Gráfico de Línea)
    UI->>UI: Renderiza Líneas de Tendencia
```

### 5.6 Flujo de Edición de un Movimiento

```mermaid
sequenceDiagram
    actor Usuario
    participant UI as Frontend (movimientos.js)
    participant API as Backend (movimientos.py)
    participant Repo as Base de Datos (SQLite)

    Usuario->>UI: Clic en icono Lápiz (Editar)
    UI->>API: GET /movimientos/{id}
    API-->>UI: 200 OK (Datos del movimiento)
    
    UI->>UI: Pre-carga los datos en el formulario (Pinta el monto y la categoría)
    
    Usuario->>UI: Cambia el monto a "8.00" y actualiza categoría
    UI->>API: PUT /movimientos/{id} (Header: Bearer Token)
    
    API->>API: Valida Token y JSON
    API->>Repo: session.merge(MovimientoActualizado)
    API->>Repo: session.commit()
    Repo-->>API: Fila actualizada
    
    API-->>UI: 200 OK
    UI->>UI: Cierra el formulario
    UI->>UI: Muestra notificación Toast (Azul/Actualización)
    UI->>UI: Llama a refreshDashboard() y lista_movimientos()
```

### 5.7 Flujo de Presupuestos y Alertas

```mermaid
sequenceDiagram
    actor Usuario
    participant UI as Frontend (presupuestos.js)
    participant API as Backend (presupuestos)
    participant Repo as Base de Datos (SQLite)

    Usuario->>UI: Define límite para "Alimentos: Q2000" y clic Guardar
    UI->>API: POST /presupuestos/ (categoria_id, limite, mes, anio)

    API->>API: Valida Token JWT y datos (limite > 0)
    API->>Repo: SELECT presupuesto WHERE user_id=? AND categoria_id=?
    Repo-->>API: Resultado (existe o no)

    alt Presupuesto nuevo
        API->>Repo: INSERT INTO presupuestos
    else Ya existe → actualizar límite
        API->>Repo: UPDATE presupuestos SET limite=?
    end

    API->>Repo: SELECT SUM(monto) FROM movimientos WHERE categoria_id=? AND tipo='gasto'
    Repo-->>API: Total gastado actual
    API->>API: Calcula pct_usado y determina estado (ok / advertencia / excedido)
    API-->>UI: 200 OK (PresupuestoResponse con estado)
    UI->>UI: Refresca lista y llama a cargarAlertas()

    Note over UI,API: Al cargar el dashboard
    UI->>API: GET /presupuestos/alertas
    API->>Repo: SELECT presupuestos WHERE user_id=?
    Repo-->>API: Lista de presupuestos
    API->>API: Filtra los que tienen pct_usado >= 75%
    API-->>UI: Lista de alertas activas
    UI->>UI: Renderiza banner con alertas 🟡/🔴
```

### 5.8 Flujo de Autenticación con JWT

```mermaid
sequenceDiagram
    participant UI as api.js (Proxy)
    participant API as FastAPI Middleware
    participant App as Lógica del Endpoint

    UI->>API: Cualquier petición protegida (Header: Authorization)
    
    API->>API: ¿El Token está presente y es válido?
    
    alt Token Válido
        API->>App: Procesa la solicitud
        App-->>UI: Respuesta exitosa
    else Token Expirado o Inválido
        API-->>UI: 401 Unauthorized
        UI->>UI: Borra localStorage (Logout proactivo)
        UI->>UI: Redirige a /login
    end
```