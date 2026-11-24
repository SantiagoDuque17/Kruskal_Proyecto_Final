-- Esquema para el Problema 1: Fibra óptica en Bogotá (Kruskal) 
-- Ejecutar en phpMyAdmin (pestaña SQL) o dejar que el script lo cargue solo.

CREATE DATABASE IF NOT EXISTS fibra_optica
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE fibra_optica;

CREATE TABLE IF NOT EXISTS localidades (
    codigo CHAR(1)      NOT NULL PRIMARY KEY,
    nombre VARCHAR(50)  NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tramos (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    origen  CHAR(1) NOT NULL,
    destino CHAR(1) NOT NULL,
    costo   INT     NOT NULL CHECK (costo > 0),   -- millones de pesos
    UNIQUE KEY uq_tramo (origen, destino),
    FOREIGN KEY (origen)  REFERENCES localidades(codigo),
    FOREIGN KEY (destino) REFERENCES localidades(codigo)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ejecuciones (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    algoritmo   VARCHAR(30) NOT NULL,
    costo_total INT         NOT NULL,
    fecha       TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pasos_ejecucion (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    ejecucion_id INT          NOT NULL,
    orden        INT          NOT NULL,
    origen       CHAR(1)      NOT NULL,
    destino      CHAR(1)      NOT NULL,
    costo        INT          NOT NULL,
    aceptado     BOOLEAN      NOT NULL,
    motivo       VARCHAR(120) NOT NULL,
    conjuntos    VARCHAR(200) NOT NULL,
    FOREIGN KEY (ejecucion_id) REFERENCES ejecuciones(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Datos del problema
INSERT IGNORE INTO localidades (codigo, nombre) VALUES
    ('U', 'Usaquén'), ('C', 'Chapinero'), ('T', 'Teusaquillo'),
    ('S', 'Suba'),    ('K', 'Kennedy'),   ('F', 'Fontibón'),
    ('B', 'Bosa');

INSERT IGNORE INTO tramos (origen, destino, costo) VALUES
    ('U', 'C', 8),  ('U', 'S', 6),  ('C', 'T', 5),  ('C', 'S', 9),
    ('T', 'F', 7),  ('F', 'B', 8),  ('T', 'K', 10), ('C', 'K', 12),
    ('S', 'F', 11), ('F', 'K', 4),  ('K', 'B', 3);