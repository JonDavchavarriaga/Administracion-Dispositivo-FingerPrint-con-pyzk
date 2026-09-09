-- Legacy bootstrap reference. Use Alembic for application schema changes.
CREATE DATABASE IF NOT EXISTS huellero_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE huellero_db;

-- Cost centers
CREATE TABLE IF NOT EXISTS cost_centers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    external_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    cost_center_id INT NULL,
    is_active TINYINT(1) DEFAULT 1,

    -- Keep the user when its cost center is deleted.
    CONSTRAINT fk_user_cost_center FOREIGN KEY (cost_center_id) REFERENCES cost_centers(id) ON DELETE SET NULL,
    INDEX idx_external_id (external_id)
) ENGINE=InnoDB;

-- Devices
CREATE TABLE IF NOT EXISTS devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    ip VARCHAR(50) NOT NULL,
    port INT DEFAULT 4370,
    interval_seconds INT NOT NULL DEFAULT 60,
    is_active TINYINT(1) DEFAULT 1,
    last_sync_at DATETIME NULL
) ENGINE=InnoDB;

-- User-device links
CREATE TABLE IF NOT EXISTS user_devices (
    user_id INT NOT NULL,
    device_id INT NOT NULL,
    PRIMARY KEY (user_id, device_id),
    CONSTRAINT fk_ud_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_ud_device FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Attendance
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    user_external_id VARCHAR(50) NOT NULL,
    device_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_att_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_att_device FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE RESTRICT,
    CONSTRAINT uq_attendance_device_external_timestamp
        UNIQUE (device_id, user_external_id, timestamp)
) ENGINE=InnoDB;