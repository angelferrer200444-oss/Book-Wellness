# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import db
import Libros as libros_api
import requests

app = Flask(__name__)
CORS(app)

api = libros_api.LibroAPI()

# -------------------------
# PÁGINAS HTML
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/buscar")
def buscar():
    texto = request.args.get("q", "")
    libros = api.buscar_libros(texto)
    return render_template("BusquedaDeLibros.html", consulta=texto, libros=libros)

@app.route("/sesion")
def sesion():
    return render_template("HTML SESION/sesion.html")

@app.route("/registro")
def registro():
    return render_template("HTML SESION/Registrarse.html")

@app.route("/recuperar-password")
def recuperar_password():
    return render_template("HTML SESION/¿OlvidasteContrasena.html")

@app.route("/libro")
def libro():
    clave = request.args.get("clave")
    portada = request.args.get("portada")

    if not clave:
        return render_template("libros.html")

    url = f"https://openlibrary.org{clave}.json"

    
    titulo = "Sin título"
    descripcion = "Descripción no disponible"
    autor = "Autor desconocido"

    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        titulo = datos.get("title", "Sin título")

        if "description" in datos:
            if isinstance(datos["description"], dict):
                descripcion = datos["description"].get("value", descripcion)
            else:
                descripcion = datos["description"]

        autor_data = datos.get("authors", [])
        if autor_data:
            autores = []
            for a in autor_data:
                if isinstance(a, dict) and "author" in a:
                    key = a["author"].get("key")
                    if key:
                        try:
                            r = requests.get(
                                f"https://openlibrary.org{key}.json",
                                timeout=10
                            )
                            if r.ok:
                                ad = r.json()
                                autores.append(ad.get("name", "Autor desconocido"))
                        except requests.exceptions.RequestException:
                            pass
            if autores:
                autor = ", ".join(autores)

    except requests.exceptions.RequestException as e:
        print("Error API:", e)

    
    return render_template(
        "libros.html",
        titulo=titulo,
        descripcion=descripcion,
        autor=autor,
        portada=portada
    )

# -------------------------
# API USUARIOS 
# -------------------------

@app.route('/api/registrar_usuario', methods=['POST'])
def registrar_usuario():
    try:
        datos = request.json
        nombre_usuario = datos.get('nombre')
        correo_usuario = datos.get('correo')
        password_usuario = datos.get('password')

        if not nombre_usuario or not correo_usuario or not password_usuario:
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        conexion = db.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, password) VALUES (%s, %s, %s)",
            (nombre_usuario, correo_usuario, password_usuario)
        )
        conexion.commit()
        id_generado = cursor.lastrowid
        cursor.close()
        conexion.close()

        return jsonify({
            "mensaje": f"¡Usuario {nombre_usuario} registrado con éxito!",
            "id_asignado": id_generado
        }), 201

    except db.mysql.connector.errors.IntegrityError:
        # 👇 Esto atrapa el error de correo duplicado
        return jsonify({"error": "Este correo ya está registrado"}), 409

    except db.mysql.connector.Error as err:
        return jsonify({"error": f"Error en MySQL: {err.msg}"}), 500

    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

@app.route('/api/login', methods=['POST'])
def login_usuario():
    datos = request.json
    correo = datos.get('correo')
    password = datos.get('password')

    if not correo or not password:
        return jsonify({"error": "Rellena todos los campos"}), 400

    usuario = db.buscar_usuario(correo, password)

    if usuario:
        return jsonify({"mensaje": f"¡Bienvenido, {usuario['nombre']}!", "usuario": usuario}), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401

# -------------------------
# EJECUCIÓN
# -------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)