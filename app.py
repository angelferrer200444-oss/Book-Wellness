from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import db
import Libros as libros_api
import requests
import time
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'ilovesucklemons'  # clave secretosa
CORS(app)

# -------------------------
# FUNCIÓN AUXILIAR PARA PETICIONES
# -------------------------

def obtener_json(url, intentos=3):

    for i in range(intentos):

        try:

            respuesta = requests.get(
                url,
                timeout=5
            )

            respuesta.raise_for_status()

            return respuesta.json()

        except requests.exceptions.RequestException:

            if i < intentos - 1:
                time.sleep(0.5)

    return None

# -------------------------
# API DE LIBROS
# -------------------------

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

# -------------------------
# BUSQUEDA LIBRO 
# -------------------------

@app.route("/buscar")
def buscar():

    texto = request.args.get("q", "")

    return render_template(
        "BusquedaDeLibros.html",
        consulta=texto
    )

@app.route("/api/buscar")
def api_buscar():

    texto = request.args.get("q", "")

    try:

        libros = api.buscar_libros(texto)

        return jsonify(libros)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -------------------------
# SESION Y LOGIN 
# -------------------------

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
# DETALLE LIBRO 
# -------------------------

@app.route("/libro")
def libro():

    clave = request.args.get("clave")
    portada = request.args.get("portada")

    return render_template(
        "libros.html",
        clave=clave,
        portada=portada
    )

@app.route("/api/libro")
def api_libro():

    clave = request.args.get("clave")

    if not clave:
        return jsonify({"error": "Clave inválida"}), 400

    titulo = "Sin título"
    subtitulo = ""
    descripcion = "Descripción no disponible"
    autor = "Autor desconocido"
    anio = "Desconocido"
    paginas = "Desconocido"
    generos = "No disponible"
    pais = "Desconocido"
    formato = "Físico"
    


    try:

        datos = obtener_json(
            f"https://openlibrary.org{clave}.json"
        )

        if not datos:

            return jsonify({
                "error": "No fue posible obtener la información"
            }), 500

        try:
            titulo = datos.get("title", titulo)
        except Exception:
            pass

        try:
            subtitulo = datos.get("subtitle")
        except Exception:
            pass

        try:
            anio = datos.get("first_publish_date")
        except Exception:
            pass


        if (
            not subtitulo
            or not anio
            or paginas == "Desconocido"
            or pais == "Desconocido"
            or formato == "Físico"
        ):

            try:

                url_ed = (
                    f"https://openlibrary.org"
                    f"{clave}/editions.json?limit=20"
                )

                ediciones = obtener_json(url_ed)

                if ediciones:

                    for ed in ediciones.get("entries", []):

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

                        if paginas == "Desconocido":

                            paginas = (
                                ed.get("number_of_pages")
                                or paginas
                            )

                        if formato == "Físico":

                            formato = (
                                ed.get("physical_format")
                                or formato
                            )

                        if pais == "Desconocido":

                            lugares = ed.get("publish_places", [])

                            if lugares:

                                if isinstance(lugares[0], dict):
                                    pais = lugares[0].get(
                                        "name",
                                        "Desconocido"
                                    )

                                else:
                                    pais = str(lugares[0])

                        if (
                            subtitulo
                            and anio
                            and paginas != "Desconocido"
                            and pais != "Desconocido"
                        ):
                            break


            except Exception:
                pass

        subtitulo = subtitulo or ""
        anio = anio or "Desconocido"

        try:

            if "description" in datos:

                if isinstance(datos["description"], dict):

                    descripcion = datos["description"].get(
                        "value",
                        descripcion
                    )

                else:

                    descripcion = datos["description"]

        except Exception:
            pass


        autores = []

        try:

            for a in datos.get("authors", []):

                if isinstance(a, dict) and "author" in a:

                    autor_key = a["author"].get("key")

                    if autor_key:

                        try:

                            datos_autor = obtener_json(
                                f"https://openlibrary.org{autor_key}.json"
                            )

                            if datos_autor:

                                autores.append(
                                    datos_autor.get(
                                        "name",
                                        "Autor desconocido"
                                    )
                                )

                        except Exception:
                            pass

        except Exception:
            pass

        if autores:

            autor = ", ".join(autores)


        try:

            subjects = datos.get("subjects", [])

            if subjects:
                generos = ", ".join(subjects[:5])

        except Exception:
            pass


        try:

            lugares = datos.get("subject_places", [])

            if lugares:
                pais = lugares[0]

        except Exception:
            pass


        try:

            formatos = datos.get("physical_format")

            if formatos:
                formato = formatos

        except Exception:
            pass



        return jsonify({

            "titulo": titulo,
            "subtitulo": subtitulo,
            "descripcion": descripcion,
            "autor": autor,
            "anio": anio,

            "paginas": paginas,
            "generos": generos,
            "pais": pais,
            "formato": formato

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# -------------------------
# FILTRO POR GÉNERO
# -------------------------

@app.route("/filtrar")
def filtrar():

    genero = request.args.get("genero", "")

    return render_template(
        "BusquedaDeLibros.html",
        consulta=genero
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
    paginas = datos.get('paginas')  

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
            key_libro,
            paginas  
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

# -------------------------
# SECCION LECTURA
# -------------------------

@app.route("/sesion-lectura")
def sesion_lectura():
    id_libro = request.args.get('id_libro')
    id_usuario = session.get('id_usuario')
    libro = None
    pagina_actual = 0
    capitulos_leidos = 0
    fecha_inicio = None
    fecha_fin = None
    fecha_limite = None
    
    if id_libro:
        libro = db.obtener_libro(id_libro)
        if id_usuario:
            lectura = db.obtener_lectura_en_progreso(id_usuario, id_libro)
            if lectura:
                pagina_actual = lectura['pagina_actual']
                capitulos_leidos = lectura['capitulos_leidos']
                fecha_inicio = lectura['fecha_inicio']
                fecha_fin = lectura['fecha_fin']
                fecha_limite = lectura['fecha_limite']
    
    datos_completos = libro and libro.get('paginas_totales') and libro.get('num_caps')
    
    return render_template(
        "seccion-lectura/sesion-lectura.html", 
        libro=libro,
        datos_completos=datos_completos,
        pagina_actual=pagina_actual,
        capitulos_leidos=capitulos_leidos,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        fecha_limite=fecha_limite
    )
    

@app.route('/api/iniciar_lectura', methods=['POST'])
def iniciar_lectura():
    datos = request.json
    id_libro = datos.get('id_libro')
    paginas_totales = datos.get('paginas_totales')
    num_caps = datos.get('num_caps')
    formato = datos.get('formato')

    try:
        db.actualizar_datos_libro(id_libro, paginas_totales, num_caps, formato)
        return jsonify({"mensaje": "Datos guardados"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/guardar_fecha_limite', methods=['POST'])
def guardar_fecha_limite_ruta():
    datos = request.json
    id_usuario = session.get('id_usuario')
    id_libro = datos.get('id_libro')
    fecha_limite = datos.get('fecha_limite')

    if not id_usuario:
        return jsonify({"error": "No hay sesión activa"}), 401

    try:
        db.guardar_fecha_limite(id_usuario, id_libro, fecha_limite)
        return jsonify({"mensaje": "Fecha límite guardada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/seccion2-lectura")
def seccion2_lectura():
    id_libro = request.args.get('id_libro')
    libro = None
    if id_libro:
        libro = db.obtener_libro(id_libro)
    return render_template("seccion-lectura/seccion2-lectura.html", libro=libro)


@app.route('/seccion3-lectura')
def seccion3_lectura():
    id_libro = request.args.get('id_libro')
    id_usuario = session.get('id_usuario')
    
    lectura = None
    if id_libro and id_usuario:
        lectura = db.obtener_lectura_en_progreso(id_usuario, id_libro)
    
    pagina_anterior = lectura['pagina_actual'] if lectura else 0
    
    return render_template(
        'seccion-lectura/seccion3-lectura.html', 
        id_libro=id_libro,
        pagina_anterior=pagina_anterior
    )


@app.route('/api/guardar_lectura', methods=['POST'])
def guardar_lectura_ruta():
    datos = request.json
    id_usuario = session.get('id_usuario')

    if not id_usuario:
        return jsonify({"error": "No hay sesión activa"}), 401

    try:
        id_lectura = db.guardar_lectura(
            id_usuario=id_usuario,
            id_libro=datos.get('id_libro'),
            tiempo_minutos=datos.get('tiempo_minutos'),
            estado=datos.get('estado', 'en progreso'),
            fecha_fin=datos.get('fecha_fin'),
            paginas_leidas=datos.get('paginas_leidas', 0),
            pagina_actual=datos.get('pagina_actual', 0),
            capitulos_leidos=datos.get('capitulos_leidos', 0)
        )

        respuestas = datos.get('respuestas', [])
        if respuestas:
            db.guardar_notas_lectura(id_lectura, respuestas)

        return jsonify({"mensaje": "Lectura guardada"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# -------------------------
# BOTONES SUPERIORES y SEGUIMIENTO
# -------------------------

@app.route("/estadisticas")
def estadisticas():
    return render_template("Botones superiores/estadisticas.html")

@app.route("/objetivo")
def objetivo():
    return render_template("Botones superiores/objetivo.html")

@app.route("/notas")
def notas():
    return render_template("Botones superiores/notas.html")

@app.route("/leidos")
def leidos():
    return render_template("Botones superiores/leidos.html")

@app.route("/seguimiento")
def seguimiento():
    return render_template("seguimiento/seguimiento.html")

# -------------------------
# AGREGAR MANUALMENTE UN LIBRO HTML
# -------------------------

@app.route("/agregar")
def agregar():
    return render_template("agregar.html")

# -------------------------
# ELIMINAR LIBRO
# -------------------------

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
