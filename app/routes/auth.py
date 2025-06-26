from flask import Blueprint, render_template, request, session, jsonify, url_for, redirect, make_response
from app.utils.database import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def buscarLogin():
    response = make_response(render_template('login.html'))
    
    # Agregar headers para prevenir caché
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

@auth_bp.route('/loginUsuario', methods=['POST'])
def login_usuario():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        usuario = request.form['usuario']
        password = request.form['password']

        #validamos que no se hallan llenado solo espacios en blanco 
        if not usuario.strip() or not password.strip():
            return jsonify({"error": "Los campos no pueden estar vacíos o solo contener espacios"}), 400

        cur.execute('SELECT * FROM "Usuarios" WHERE usuario = %s AND contraseña = %s', (usuario, password))
        user = cur.fetchone()
        
        if user:
            # Si el login es exitoso, almacena el ID del usuario y el nombre de usuario en la sesión
            session['id'] = user[0] # Almacena el ID real del usuario si lo tienes
            session['usuario'] = user[2] # Almacena el nombre de usuario
            return jsonify({"message": "Inicio de sesión exitoso", "redirect": url_for('main.index')}), 200 # O a la página principal
        else:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
    except Exception as e:
        return jsonify({"error": f"Error al iniciar sesión: {str(e)}"}), 500
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()

@auth_bp.route('/register')
def registrar():
    response = make_response(render_template('register.html'))
    
    # Agregar headers para prevenir caché
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

@auth_bp.route('/registrarUsuario', methods=['POST'])
def guardar_usuario():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Aquí se obtiene los datos del usuario desde el request
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        email = request.form['email']
        password = request.form['password']

        #validamos que no se hallan llenado solo espacios en blanco 
        if not nombre.strip() or not usuario.strip() or not email.strip() or not password.strip():
            return jsonify({"error": "Los campos no pueden estar vacíos o solo contener espacios"}), 400

        #Vamos a validar que el nombre no este vacio
        if not nombre:
            return jsonify({"error": "El nombre no puede estar vacío"}), 400
        #Vamos a validar que el usuario no este vacio
        if not usuario:
            return jsonify({"error": "El usuario no puede estar vacío"}), 400
        
        #Vamos a validar que el email no este vacio
        if not email:
            return jsonify({"error": "El email no puede estar vacío"}), 400
        #Vamos a validar que la contraseña no este vacia
        if not password:
            return jsonify({"error": "La contraseña no puede estar vacía"}), 400

        #vamos a validar que el usuario no exista
        cur.execute('SELECT * FROM "Usuarios" WHERE usuario = %s', (usuario,))
        existing_user = cur.fetchone()
        if existing_user:
            return jsonify({"error": "El usuario ya existe"}), 400

        cur.execute('INSERT INTO "Usuarios" (nombre, usuario, email, contraseña) VALUES (%s, %s, %s, %s)', (nombre, usuario, email, password))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Usuario guardado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al guardar el usuario: {str(e)}"}), 500 

@auth_bp.route('/check-auth')
def check_auth():
    """Ruta para verificar si el usuario está autenticado"""
    if 'usuario' in session:
        return jsonify({"authenticated": True, "user": session.get('usuario')}), 200
    else:
        return jsonify({"authenticated": False}), 401

@auth_bp.route('/logout')
def logout():
    # Limpiar toda la sesión
    session.clear()
    
    # Crear respuesta de redirección con headers de caché
    response = redirect(url_for('auth.buscarLogin'))
    
    # Agregar headers para prevenir caché en la página de login después del logout
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response