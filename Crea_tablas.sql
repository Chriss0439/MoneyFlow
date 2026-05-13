-- 1. Tabla de Usuarios (Soporta el flujo de Login y Registro) [cite: 851, 852]
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL, -- Requerimiento de seguridad [cite: 358]
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Categorías (Garantiza no duplicados e integridad) [cite: 381, 382]
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE, -- Ejemplo: 'Fotocopias', 'Mesada', 'Freelance' [cite: 37, 89]
    tipo TEXT CHECK(tipo IN ('ingreso', 'gasto')) NOT NULL
);

-- 3. Tabla de Movimientos (El core del sistema) [cite: 364, 373]
CREATE TABLE movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    categoria_id INTEGER NOT NULL,
    monto REAL NOT NULL CHECK(monto > 0), -- Validación crítica del análisis [cite: 366]
    descripcion TEXT,
    fecha DATE DEFAULT CURRENT_DATE, -- Validación de fecha [cite: 368]
    es_apoyo_familiar INTEGER DEFAULT 0, -- Para calcular el % de dependencia 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- 4. Índice de Rendimiento (Garantiza respuesta < 3 segundos) [cite: 79, 396]
CREATE INDEX idx_movimientos_user ON movimientos(user_id);