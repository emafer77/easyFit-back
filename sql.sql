CREATE TABLE objetivos (
    id SERIAL PRIMARY KEY, 
    nombre VARCHAR(100) NOT NULL,  
    descripcion TEXT  
);

CREATE TABLE niveles_ejercicio (
    id SERIAL PRIMARY KEY, 
    nivel VARCHAR(50) NOT NULL, 
    descripcion TEXT  
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY, 
    nombre VARCHAR(100) NOT NULL, 
    apellidos VARCHAR(100) NOT NULL, 
    correo TEXT UNIQUE NOT NULL, 
    contrasena TEXT NOT NULL, 
    telefono TEXT,  
    edad SMALLINT,  
    genero VARCHAR(10), 
    peso DECIMAL(7, 2), 
    altura DECIMAL(5, 2), 
    objetivo_id INT REFERENCES objetivos(id),  
    nivel_ejercicio_id INT REFERENCES niveles_ejercicio(id),  
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP  
);

CREATE TABLE membresias (
    id SERIAL PRIMARY KEY,  
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE, 
    estado VARCHAR(10) DEFAULT 'activa' CHECK (estado IN ('activa', 'inactiva')),  
    fecha_inicio TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,  
    fecha_expiracion TIMESTAMP WITH TIME ZONE,  
    CONSTRAINT chk_fecha_expiracion CHECK (fecha_expiracion > fecha_inicio)  
);

CREATE OR REPLACE FUNCTION actualizar_estado_membresia()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.fecha_expiracion < CURRENT_TIMESTAMP AND NEW.estado = 'activa' THEN
        NEW.estado := 'inactiva';  
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_membresia
BEFORE INSERT OR UPDATE ON membresias
FOR EACH ROW
EXECUTE FUNCTION actualizar_estado_membresia();

CREATE TABLE musculos (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE ejercicios (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_musculo BIGINT REFERENCES musculos (id) ON DELETE SET NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT
);

CREATE TABLE categorias_ejercicios (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT
);

ALTER TABLE ejercicios
ADD COLUMN id_categoria BIGINT REFERENCES categorias_ejercicios (id) ON DELETE SET NULL;

CREATE TABLE ejercicio_videos (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    ejercicio_id BIGINT REFERENCES ejercicios (id) ON DELETE CASCADE,
    video_url TEXT NOT NULL UNIQUE
);

CREATE TABLE ejercicio_imagenes (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    ejercicio_id BIGINT REFERENCES ejercicios (id) ON DELETE CASCADE,
    image_url TEXT NOT NULL UNIQUE 
);

CREATE TABLE rutinas (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre TEXT NOT NULL UNIQUE,
    tipo_rutina TEXT
);

CREATE TABLE rutinas_musculos (
    id_rutina BIGINT REFERENCES rutinas (id) ON DELETE CASCADE,
    id_musculo BIGINT REFERENCES musculos (id) ON DELETE CASCADE,
    PRIMARY KEY (id_rutina, id_musculo)
);

CREATE TABLE rutinas_ejercicios (
    id_rutina BIGINT REFERENCES rutinas (id) ON DELETE CASCADE,
    id_ejercicio BIGINT REFERENCES ejercicios (id) ON DELETE CASCADE,
    repeticiones INT NOT NULL CHECK (repeticiones > 0),
    PRIMARY KEY (id_rutina, id_ejercicio)
);

ALTER TABLE rutinas
ADD COLUMN descripcion TEXT;

CREATE TABLE niveles_rutinas (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre_nivel TEXT NOT NULL UNIQUE,
    repeticiones INT CHECK (repeticiones > 0),
    tiempo_descanso INT CHECK (tiempo_descanso >= 0),
    recomendacion_peso TEXT,
    id_rutina BIGINT REFERENCES rutinas (id) ON DELETE CASCADE
);

INSERT INTO objetivos (id, nombre) VALUES (1, 'Ganar musculo');
INSERT INTO objetivos (id, nombre) VALUES (2, 'Perder grasa');
INSERT INTO objetivos (id, nombre) VALUES (3, 'Mejorar salud');

INSERT INTO niveles_ejercicio (id, nivel) VALUES (1, 'Principiante');
INSERT INTO niveles_ejercicio (id, nivel) VALUES (2, 'Intermedio');
INSERT INTO niveles_ejercicio (id, nivel) VALUES (3, 'Avanzado');

INSERT INTO musculos (nombre) VALUES ('pecho');
INSERT INTO musculos (nombre) VALUES ('biceps');
INSERT INTO musculos (nombre) VALUES ('triceps');
INSERT INTO musculos (nombre) VALUES ('abdominales');
INSERT INTO musculos (nombre) VALUES ('gluteos');
INSERT INTO musculos (nombre) VALUES ('pierna');
INSERT INTO musculos (nombre) VALUES ('espalda');
INSERT INTO musculos (nombre) VALUES ('hombro');

INSERT INTO categorias_ejercicios ( nombre, descripcion) VALUES ( 'cardio', 'Ejercicios de cardio');
INSERT INTO categorias_ejercicios ( nombre, descripcion) VALUES ( 'resistencia', 'Ejercicios de resistencia');
INSERT INTO categorias_ejercicios ( nombre, descripcion) VALUES ('flexibilidad', 'Ejercicios de flexibilidad');
INSERT INTO categorias_ejercicios ( nombre, descripcion) VALUES ( 'fuerza', 'Ejercicios de fuerza');