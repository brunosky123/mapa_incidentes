from flask import Flask, jsonify, render_template
import psycopg2
import json

from flask_cors import CORS

# Configurar Flask para usar la carpeta 'plantillas' soy un nuevo comentario
app = Flask(__name__, static_folder='static', template_folder='plantillas')
CORS(app)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="rutas_seguras",
            user="e_bruno",
            password="12345678",
            host="127.0.0.1",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/segura')
def buscarSegura():
    return render_template('ruta_segura.html')

@app.route('/segura2')
def buscarSegura2():
    return render_template('ruta_segura2.html')

@app.route('/login')
def buscarLogin():
    return render_template('login.html')

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
        username = request.form['username']
        password = request.form['password']

        cur.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, password))
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
