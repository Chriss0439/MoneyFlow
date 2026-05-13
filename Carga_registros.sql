-- Insertar categorías por defecto [cite: 449]
INSERT INTO categorias (nombre, tipo) VALUES ('Apoyo Familiar', 'ingreso');
INSERT INTO categorias (nombre, tipo) VALUES ('Freelance/Emprendimiento', 'ingreso');
INSERT INTO categorias (nombre, tipo) VALUES ('Fotocopias y Libros', 'gasto');
INSERT INTO categorias (nombre, tipo) VALUES ('Alimentación/Cafetería', 'gasto');
INSERT INTO categorias (nombre, tipo) VALUES ('Transporte', 'gasto');

-- Insertar usuario de prueba para el Login [cite: 356]
INSERT INTO users (nombre, correo, password_hash) 
VALUES ('Usuario Beta', 'estudiante@u.edu.gt', 'argon2_hashed_password');