from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import db
import Libros as libros_api
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'ilovesucklemons'  # clave secretosa
CORS(app)


api = libros_api.LibroAPI()

# -------------------------
# PÁGINAS HTML
# -------------------------

@app.route("/")
def home():

    libros_leyendo = []
    libros_pendientes = []

    id_usuario = session.get('id_usuario')
    

    if id_usuario:
        libros_leyendo = db.obtener_libros_usuario(id_usuario, 'leyendo')
        libros_pendientes = db.obtener_libros_usuario(id_usuario, 'pendiente')

    return render_template(
        'index.html',
        libros_leyendo=libros_leyendo,
        libros_pendientes=libros_pendientes
    )


@app.route("/buscar")
def buscar():

    texto = request.args.get("q", "")
    libros = api.buscar_libros(texto)

    return render_template(
        "BusquedaDeLibros.html",
        consulta=texto,
        libros=libros
    )


@app.route("/sesion")
def sesion():
    return render_template("HTML SESION/sesion.html")


@app.route("/registro")
def registro():
    return render_template("HTML SESION/Registrarse.html")


@app.route("/recuperar-password")
def recuperar_password():
    return render_template("HTML SESION/¿OlvidasteContrasena.html")

@app.route('/seccion-lectura')
def seccion_lectura():

    return render_template(
        'seccion-lectura/Seccion2-Lectura.html'
    )

# -------------------------
# DETALLE LIBRO (MEJORADO)
# -------------------------

@app.route("/libro")
def libro():

    clave = request.args.get("clave")
    portada = request.args.get("portada")
    print("CLAVE RECIBIDA:", clave) 

    if not clave:
        return render_template("libros.html")

    url = f"https://openlibrary.org{clave}.json"

    titulo = "Sin título"
    subtitulo = ""
    descripcion = "Descripción no disponible"
    autor = "Autor desconocido"
    anio = "Desconocido"
    key=clave

    try:

        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        # -------------------------
        # TITULO
        # -------------------------
        titulo = datos.get("title", "Sin título")

        # -------------------------
        # SUBTITULO + AÑO
        # -------------------------
        subtitulo = datos.get("subtitle")
        anio = datos.get("first_publish_date")

        # Si falta info, buscar en ediciones
        if not subtitulo or not anio:

            try:

                ediciones_url = f"https://openlibrary.org{clave}/editions.json?limit=20"
                r_ed = requests.get(ediciones_url, timeout=10)

                if r_ed.ok:

                    ediciones = r_ed.json().get("entries", [])

                    for ed in ediciones:

                        if not subtitulo:
                            subtitulo = ed.get("subtitle")

                        if not anio:
                            anio = (
                                ed.get("publish_date")
                                or (
                                    ed.get("publish_year")[0]
                                    if ed.get("publish_year")
                                    else None
                                )
                            )

                        if subtitulo and anio:
                            break

            except requests.exceptions.RequestException:
                pass

        subtitulo = subtitulo or ""
        anio = anio or "Desconocido"

        # -------------------------
        # DESCRIPCIÓN
        # -------------------------
        if "description" in datos:

            if isinstance(datos["description"], dict):
                descripcion = datos["description"].get(
                    "value",
                    descripcion
                )
            else:
                descripcion = datos["description"]

        # -------------------------
        # AUTORES
        # -------------------------
        autor_data = datos.get("authors", [])

        if autor_data:

            autores = []

            for a in autor_data:

                if isinstance(a, dict) and "author" in a:

                    autor_key = a["author"].get("key")

                    if autor_key:

                        try:

                            r = requests.get(
                                f"https://openlibrary.org{autor_key}.json",
                                timeout=10
                            )

                            if r.ok:

                                ad = r.json()

                                autores.append(
                                    ad.get(
                                        "name",
                                        "Autor desconocido"
                                    )
                                )

                        except requests.exceptions.RequestException:
                            pass

            if autores:
                autor = ", ".join(autores)

    except requests.exceptions.RequestException as e:
        print("Error API:", e)

    print("KEY QUE SE PASA AL TEMPLATE:", key)

    return render_template(
        "libros.html",
        titulo=titulo,
        subtitulo=subtitulo,
        descripcion=descripcion,
        autor=autor,
        portada=portada,
        anio=anio,
        key=key
    )


# -------------------------
# FILTRO POR GÉNERO
# -------------------------

@app.route("/filtrar")
def filtrar():

    genero = request.args.get("genero")

    libros = api.buscar_libros(genero)

    return render_template(
        "BusquedaDeLibros.html",
        consulta=genero,
        libros=libros
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
            return jsonify({
                "error": "Todos los campos son obligatorios"
            }), 400

        conexion = db.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios
            (nombre, correo, password)
            VALUES (%s, %s, %s)
            """,
            (
                nombre_usuario,
                correo_usuario,
                password_usuario
            )
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

        return jsonify({
            "error": "Este correo ya está registrado"
        }), 409

    except db.mysql.connector.Error as err:

        return jsonify({
            "error": f"Error en MySQL: {err.msg}"
        }), 500

    except Exception as e:

        return jsonify({
            "error": f"Error inesperado: {str(e)}"
        }), 500


@app.route('/api/login', methods=['POST'])
def login_usuario():
    datos = request.json
    correo = datos.get('correo')
    password = datos.get('password')

    if not correo or not password:
        return jsonify({"error": "Rellena todos los campos"}), 400

    usuario = db.buscar_usuario(correo, password)  

    if usuario:                                     
        session['id_usuario'] = usuario['id_usuario']
        session['nombre'] = usuario['nombre']
        return jsonify({
            "mensaje": f"¡Bienvenido, {usuario['nombre']}!",
            "usuario": usuario
        }), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada"}), 200

# -------------------------
# BOOK TRACKER
# -------------------------

@app.route('/api/agregar_libro', methods=['POST'])
def agregar_libro():

    datos = request.json

    id_usuario = datos.get('id_usuario')
    titulo = datos.get('titulo')
    autor = datos.get('autor')
    descripcion = datos.get('descripcion')
    portada = datos.get('portada')
    categoria = datos.get('categoria', 'pendiente')
    key_libro = datos.get('key_libro')

    if not id_usuario:
        return jsonify({
            "error": "Usuario no identificado"
        }), 400

    try:

        resultado = db.agregar_libro(
            id_usuario,
            titulo,
            autor,
            descripcion,
            portada,
            categoria,
            key_libro
        )

        if resultado:

            return jsonify({
                "mensaje": "Libro agregado correctamente"
            }), 201

        return jsonify({
            "error": "Este libro ya está en tu lista"
        }), 409

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    
@app.route("/sesion-lectura")
def sesion_lectura():
    return render_template("seccion-lectura/sesion-lectura.html")

@app.route('/seccion3-lectura')
def seccion3_lectura():
    return render_template(
        'seccion-lectura/seccion3-lectura.html')


@app.route('/api/eliminar_libro', methods=['DELETE'])
def eliminar_libro():
    datos = request.json
    id_libro = datos.get('id_libro')
    id_usuario = datos.get('id_usuario')

    if not id_libro or not id_usuario:
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        db.eliminar_libro(int(id_libro), int(id_usuario))  # 👈 convertir a int
        return jsonify({"mensaje": "Libro eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# EJECUCIÓN
# -------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
