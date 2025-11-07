-- Crear rol
CREATE ROLE bitacora_user WITH LOGIN PASSWORD 'bitacora_pass' CREATEDB;

-- Crear BD
CREATE DATABASE bitacora_db WITH OWNER bitacora_user;

-- Conectarse a la BD y crear tabla
\c bitacora_db

-- Tabla de bitácoras
CREATE TABLE registros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    severidad VARCHAR(20) DEFAULT 'BAJA',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dar permisos
GRANT ALL PRIVILEGES ON TABLE bitacoras TO bitacora_user;
GRANT ALL PRIVILEGES ON SEQUENCE bitacoras_id_seq TO bitacora_user;
GRANT USAGE, CREATE ON SCHEMA public TO bitacora_user;

-- Verificar
\dt
