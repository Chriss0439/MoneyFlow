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

La base de datos utiliza **SQLite** y es administrada a través del ORM SQLAlchemy. Se compone de 3 tablas principales fuertemente tipadas y relacionadas entre sí.

```mermaid
erDiagram
    USERS ||--o{ MOVIMIENTOS : registra
    CATEGORIAS ||--o{ MOVIMIENTOS : clasifica

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
   * Agrega matemáticamente los datos del usuario para mostrar su saldo real actual, sumando ingresos y restando gastos.
3. **Movimientos (`movimientos`):**
   * Núcleo del sistema. Implementa el CRUD (Crear, Leer, Eliminar) para el flujo de dinero, incluyendo el filtrado avanzado por fecha o categoría.
4. **Reportes (`reportes`):**
   * Realiza agrupaciones (GROUP BY) en base de datos para sumar el total gastado en cada categoría y alimentar los gráficos de Chart.js.

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
* `dashboard.js`: Lee los resúmenes, pinta las tarjetas y dibuja el gráfico de torta de Chart.js usando un Canvas HTML5.
* `movimientos.js`: Dinamiza el `select` de categorías basado en si seleccionaste un gasto o un ingreso.
* `categorias.js`: Lista visualmente las fuentes de ingreso y tipos de gastos.

---

## 5. Diagramas de Secuencia:

### 5.1 Flujo de Inicio de Sesión

A continuación se grafica el ciclo de vida completo de un evento común: el usuario iniciando sesión en la aplicación.

```mermaid
sequenceDiagram
    actor Usuario
    participant UI as Frontend (UI/JS)
    participant API as Backend (FastAPI)
    participant Repo as Base de Datos (SQLite)

    Usuario->>UI: Clic en botón "Login"
    UI->>API: GET /categorias/
    API-->>UI: Devuelve lista de categorías
    UI->>Usuario: Muestra formulario

    Usuario->>UI: Llena correo, elige "Transporte" y clic Guardar
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

### 5.2 Flujo de Registro de un Usuario

A continuación se grafica el ciclo de vida completo de un evento común: el usuario registrando un nuevo usuario en la aplicación.

```mermaid
sequenceDiagram
    actor Usuario
    participant UI as Frontend (UI/JS)
    participant API as Backend (FastAPI)
    participant Repo as Base de Datos (SQLite)

    Usuario->>UI: Clic en botón "Registrarse"
    UI->>API: GET /categorias/
    API-->>UI: Devuelve lista de categorías
    UI->>Usuario: Muestra formulario

    Usuario->>UI: Llena correo, elige "Transporte" y clic Guardar
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
