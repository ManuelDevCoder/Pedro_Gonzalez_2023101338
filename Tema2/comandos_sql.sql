-- Script para crear la base de datos y tablas para la aplicación de venta de ganado

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS ganaderia_db;
USE ganaderia_db;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(255) UNIQUE NOT NULL,
    contrasena CHAR(64) NOT NULL
);

-- Tabla para solicitudes de contacto de ganado
CREATE TABLE IF NOT EXISTS solicitudes_contacto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(255) NOT NULL,
    correo_electronico VARCHAR(255) NOT NULL,
    celular VARCHAR(50) NOT NULL,
    horario_llamada VARCHAR(100),
    tipo_ganado VARCHAR(100),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);