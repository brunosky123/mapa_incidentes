from flask import Flask, jsonify, render_template
import psycopg2
import json

# Configurar Flask para usar la carpeta 'plantillas' hola jeje
app = Flask(__name__, template_folder='plantillas')

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
