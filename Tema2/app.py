from flask import Flask, render_template, request, redirect, url_for, session
from db_connection import get_db_connection
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'mi_secreto'

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Ruta para el dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

# Ruta para la página de Ganado (Lotes)
@app.route('/ganado', methods=['GET', 'POST'])
def ganado():
    message = None
    message_type = None
    
    if request.method == 'POST':
        # 1. Recoger datos del formulario
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        call_time = request.form.get('call_time')
        ganado_type = request.form.get('ganado_type') # Tipo de ganado de interés

        if not all([full_name, email, phone]):
            message = "Por favor, complete todos los campos obligatorios (Nombre, Correo, Celular)."
            message_type = 'error'
        else:
            # 2. Guardar en la base de datos
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                query = """
                INSERT INTO solicitudes_contacto (nombre_completo, correo_electronico, celular, horario_llamada, tipo_ganado) 
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (full_name, email, phone, call_time, ganado_type))
                conn.commit()
                
                message = "¡Solicitud de información enviada con éxito! Nos pondremos en contacto contigo pronto."
                message_type = 'success'
                
            except mysql.connector.Error as err:
                message = f"Error al guardar la solicitud: {err}"
                message_type = 'error'
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()

    # Datos de ejemplo para mostrar los lotes (Hardcoded ya que no hay DB de productos)
    cattle_lots = [
        {"name": "Ternero/a", "quantity": 50, "price": "Consultar", "details": "Bovino joven, al pie de la madre. Excelente genética.", "image": url_for('static', filename='img/ternero.jpg')},
        {"name": "Novillito", "quantity": 30, "price": "Consultar", "details": "Macho castrado de destete hasta 2 años. Ideal para engorde.", "image": url_for('static', filename='img/novillito.jpg')},
        {"name": "Novillo", "quantity": 20, "price": "Consultar", "details": "Macho castrado de más de 2 años. Alto rendimiento cárnico.", "image": url_for('static', filename='img/novillo.jpg')},
        {"name": "Vaquillona", "quantity": 45, "price": "Consultar", "details": "Hembra desde el destete hasta su primera parición. Futuras madres.", "image": url_for('static', filename='img/vaquillona.jpg')},
        {"name": "Vaca", "quantity": 15, "price": "Consultar", "details": "Hembra adulta. Lotes de descarte o vientres productivos.", "image": url_for('static', filename='img/vaca.jpg')},
        {"name": "Toro", "quantity": 5, "price": "Consultar", "details": "Macho entero. Reproductores de alta calidad genética.", "image": url_for('static', filename='img/toro.jpg')},
    ]

    return render_template('ganado.html', 
                           cattle_lots=cattle_lots, 
                           message=message, 
                           message_type=message_type)


@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

# Ruta para registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    message_type = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash de la contraseña
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar usuario en la base de datos
        query = "INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (%s, %s)"
        try:
            cursor.execute(query, (username, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()
            # Almacenar mensaje de éxito en la sesión para mostrarlo en la página de login
            session['flash_message'] = "Registro exitoso. Por favor, inicia sesión."
            session['flash_message_type'] = 'success'
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            if err.errno == 1062: # Error de entrada duplicada
                message = "El nombre de usuario ya existe."
                message_type = 'error'
            else:
                message = f"Error al registrar: {err}"
                message_type = 'error'
            cursor.close()
            conn.close()
            return render_template('register.html', message=message, message_type=message_type)
    
    return render_template('register.html', message=message, message_type=message_type)

# Ruta para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    message_type = None

    # Verificar si hay mensajes flash de redirecciones anteriores (ej. registro exitoso)
    if 'flash_message' in session:
        message = session.pop('flash_message')
        message_type = session.pop('flash_message_type', 'info')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash de la contraseña
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar usuario y contraseña
        query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            message = "Usuario o contraseña incorrectos"
            message_type = 'error'
            return render_template('login.html', message=message, message_type=message_type)

    return render_template('login.html', message=message, message_type=message_type)

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    session['flash_message'] = "Has cerrado sesión."
    session['flash_message_type'] = 'info'
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)