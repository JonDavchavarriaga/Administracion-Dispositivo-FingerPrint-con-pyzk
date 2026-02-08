-- 1. Configuración inicial
CREATE DATABASE IF NOT EXISTS huellero_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE huellero_db;

-- TABLA: Centros de Costos
CREATE TABLE IF NOT EXISTS cost_centers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 3. Tabla de Usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    external_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    cost_center_id INT NULL,
    is_active TINYINT(1) DEFAULT 1,

    -- Relación con Centro de Costos (Si se borra el centro, el usuario queda NULL, no se borra)
    CONSTRAINT fk_user_cost_center FOREIGN KEY (cost_center_id) REFERENCES cost_centers(id) ON DELETE SET NULL,
    INDEX idx_external_id (external_id)
) ENGINE=InnoDB;

-- 4. Tabla de Dispositivos
CREATE TABLE IF NOT EXISTS devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    ip VARCHAR(50) NOT NULL,
    port INT DEFAULT 4370,
    interval_seconds INT NOT NULL DEFAULT 60,
    is_active TINYINT(1) DEFAULT 1,
    last_sync_at DATETIME NULL
) ENGINE=InnoDB;

-- 5. Tabla Intermedia: Usuarios <-> Dispositivos
CREATE TABLE IF NOT EXISTS user_devices (
    user_id INT NOT NULL,
    device_id INT NOT NULL,
    PRIMARY KEY (user_id, device_id),
    CONSTRAINT fk_ud_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_ud_device FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 6. Tabla de Asistencia (Attendance)
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    device_id INT NOT NULL,
    timestamp DATETIME NOT NULL, -- Hora del reloj (biométrico)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Hora de guardado en servidor

    CONSTRAINT fk_att_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_att_device FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE RESTRICT
) ENGINE=InnoDB;