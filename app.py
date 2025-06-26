# ARCHIVO ORIGINAL COMENTADO - USAR run.py PARA LA NUEVA ESTRUCTURA MODULAR
# =============================================================================
# Este archivo ha sido comentado para evitar conflictos con la nueva estructura
# modular. Para ejecutar la aplicación, usa: python run.py
# =============================================================================

"""
# CÓDIGO ORIGINAL COMENTADO
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import psycopg2
import json
import os
from flask_cors import CORS
from functools import wraps

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

# Configurar Flask para usar la carpeta 'plantillas'
app = Flask(__name__, static_folder='static', template_folder='plantillas')
CORS(app)

# Configurar la clave secreta desde variables de entorno
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_secreta_por_defecto')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica si el 'usuario' está en la sesión
        if 'usuario' not in session:
            # Si no está autenticado, redirige a la página de login
            # y guarda la URL original para redirigir después del login (opcional pero bueno para UX)
            return redirect(url_for('buscarLogin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/principal')
@login_required # ¡Protegida!
def saludar():
    return render_template('index.html')

@app.route('/segura')
@login_required # ¡Protegida!
def buscarSegura():
    return render_template('ruta_segura.html')

@app.route('/segura2')
@login_required # ¡Protegida!
def buscarSegura2():
    return render_template('ruta_segura2.html')

@app.route('/login')
def buscarLogin():
    return render_template('login.html')


@app.route('/loginUsuario', methods=['POST'])
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
            session['usuario'] = user[1] # Almacena el nombre de usuario
            return jsonify({"message": "Inicio de sesión exitoso", "redirect": url_for('index')}), 200 # O a la página principal
        else:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
    except Exception as e:
        return jsonify({"error": f"Error al iniciar sesión: {str(e)}"}), 500
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()
        

@app.route('/register')
def registrar():
    return render_template('register.html')

#vamos crear un ruta para guardar un usuario
@app.route('/registrarUsuario', methods=['POST'])
def guardar_usuario():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Aquí deberías obtener los datos del usuario desde el request
        # Por ejemplo, usando request.form['username'] para obtener el nombre de usuario
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




@app.route('/incidentes')
def get_incidentes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, tipo, fecha, latitud, longitud, descripcion, ST_AsGeoJSON(ubicacion) AS ubicacion FROM incidentes")
        rows = cur.fetchall()
        features = []
        for row in rows:
            try:
                feature = {
                    "type": "Feature",
                    "properties": {
                        "id": row[0],
                        "tipo": row[1],
                        "fecha": str(row[2]),
                        "latitud": float(row[3]),
                        "longitud": float(row[4]),
                        "descripcion": row[5]
                    },
                    "geometry": json.loads(row[6])
                }
                features.append(feature)
            except Exception as e:
                print(f"Error al procesar incidente {row}: {e}")
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        cur.close()
        conn.close()
        return jsonify(geojson)
    except Exception as e:
        return jsonify({"error": f"Error al obtener incidentes: {str(e)}"}), 500

@app.route('/zonas_seguridad')
def get_zonas_seguridad():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, descripcion, ST_AsGeoJSON(area) AS area FROM zonas_seguridad")
        rows = cur.fetchall()
        features = []
        for row in rows:
            try:
                feature = {
                    "type": "Feature",
                    "properties": {
                        "id": row[0],
                        "nombre": row[1],
                        "descripcion": row[2]
                    },
                    "geometry": json.loads(row[3])
                }
                features.append(feature)
            except Exception as e:
                print(f"Error al procesar zona de seguridad {row}: {e}")
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        cur.close()
        conn.close()
        return jsonify(geojson)
    except Exception as e:
        return jsonify({"error": f"Error al obtener zonas de seguridad: {str(e)}"}), 500

@app.route('/zonas_peligrosas')
def get_zonas_peligrosas():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, descripcion, ST_AsGeoJSON(area) AS area FROM zonas_peligrosas")
        rows = cur.fetchall()
        features = []
        for row in rows:
            try:
                feature = {
                    "type": "Feature",
                    "properties": {
                        "id": row[0],
                        "nombre": row[1],
                        "descripcion": row[2]
                    },
                    "geometry": json.loads(row[3])
                }
                features.append(feature)
            except Exception as e:
                print(f"Error al procesar zona peligrosa {row}: {e}")
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        cur.close()
        conn.close()
        return jsonify(geojson)
    except Exception as e:
        return jsonify({"error": f"Error al obtener zonas peligrosas: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
"""

# =============================================================================
# INSTRUCCIONES PARA USAR LA NUEVA ESTRUCTURA MODULAR:
# =============================================================================
# 1. Ejecutar la aplicación: python run.py
# 2. Las rutas siguen siendo las mismas
# 3. La funcionalidad es idéntica pero mejor organizada
# 4. Para volver al archivo original, descomenta el código arriba
# =============================================================================
