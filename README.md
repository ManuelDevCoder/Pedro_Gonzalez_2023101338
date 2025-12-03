# Vakapipopo Ganadería - Sistema Web de Comercialización de Ganado

Este es un sistema web simple desarrollado con Flask (Python) y MySQL (a través de Docker) para la gestión y comercialización de lotes de ganado. Permite a los usuarios registrarse, iniciar sesión, ver los lotes disponibles y enviar solicitudes de contacto.

## ⚙️ Requisitos Previos

Asegúrate de tener instalado lo siguiente en tu sistema:

1.  **Python 3.x**
2.  **pip** (Administrador de paquetes de Python)
3.  **Docker** y **Docker Compose** (Necesario para levantar la base de datos MySQL)

## 🛠️ Configuración e Instalación

Sigue estos pasos para poner en marcha la aplicación localmente.

### 1. Clonar el Repositorio

```bash
git clone https://github.com/ManuelDevCoder/Pedro_Gonzalez_2023101338
cd Pedro_Gonzalez_2023101338
```

### 2. Configurar la Base de Datos (MySQL con Docker)

Utilizamos Docker Compose para levantar la base de datos MySQL.

1.  **Iniciar el Contenedor de la Base de Datos:**
    Ejecuta el siguiente comando en el directorio raíz del proyecto. Esto creará un servicio llamado `ganaderia` con la base de datos `ganaderia_db`.

    ```bash
    docker-compose up
    ```

2.  **Crear Tablas Iniciales:**
    Una vez que el contenedor esté corriendo, debes ejecutar el script SQL para crear las tablas `usuarios` y `solicitudes_contacto`.

    Conéctate a la base de datos MySQL (usando un cliente como MySQL Workbench, DBeaver, o la CLI de Docker) y ejecuta los comandos contenidos en el archivo `comandos_sql.sql`.

    **Detalles de Conexión:**
    *   Host: `localhost` (o `ganaderia` si te conectas desde otro contenedor)
    *   Puerto: `3306`
    *   Usuario: `root`
    *   Contraseña: `1234`
    *   Base de Datos: `ganaderia_db`

### 3. Configurar el Entorno Python

1.  **Instalar Dependencias de Python:**
    Instala los paquetes necesarios (`Flask` y `mysql-connector-python`).

    ```bash
    pip install -r requeriments.txt
    # Si no tienes requeriments.txt, usa:
    # pip install Flask mysql-connector-python
    ```

2.  **Verificar Conexión a la DB:**
    Asegúrate de que el archivo `db_connection.py` esté configurado para conectarse al host de Docker (`host='ganaderia'`).

### 4. Ejecutar la Aplicación

Ejecuta el servidor de Flask:

```bash
python app.py
```

La aplicación estará disponible en `http://127.0.0.1:5000/`.
