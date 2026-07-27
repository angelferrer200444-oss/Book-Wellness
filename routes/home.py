from flask import render_template
from flask import request
from flask import session
from flask import jsonify

import db
from models.Preferencias import Preferencias

def registrar_rutas(app):

    # -------------------------
    # PÁGINA PRINCIPAL
    # -------------------------

    @app.route("/")
    def home():
        libros_leyendo = []
        libros_pendientes = []
        racha_actual = 0

        id_usuario = session.get("id_usuario")

        if id_usuario:
            libros_leyendo = db.obtener_libros_usuario(id_usuario, "leyendo")
            libros_pendientes = db.obtener_libros_usuario(id_usuario, "pendiente")
            perfil = db.obtener_perfil_lectura(id_usuario)
            racha_actual = perfil['racha_actual']

        return render_template(
            "index.html",
            libros_leyendo=libros_leyendo,
            libros_pendientes=libros_pendientes,
            racha_actual=racha_actual
        )


    # -------------------------
    # SESIÓN
    # -------------------------

    @app.route("/sesion")
    def sesion():
        return render_template(
            "HTML SESION/sesion.html"
        )


    @app.route("/registro")
    def registro():
        return render_template(
            "HTML SESION/Registrarse.html"
        )


    @app.route("/recuperar-password")
    def recuperar_password():
        return render_template(
            "HTML SESION/¿OlvidasteContrasena.html"
        )


    @app.route("/seccion-lectura")
    def seccion_lectura():
        return render_template(
            "seccion-lectura/Seccion2-Lectura.html"
        )


    # -------------------------
    # BOTONES SUPERIORES
    # -------------------------
    @app.route("/estadisticas")
    def estadisticas():
        id_usuario = session.get('id_usuario')
        perfil = db.obtener_perfil_lectura(id_usuario) if id_usuario else None
        return render_template(
            "Botones superiores/estadisticas.html",
            perfil=perfil
        )


    @app.route("/objetivo")
    def objetivo():
        return render_template(
            "Botones superiores/objetivo.html"
        )


    @app.route("/leidos")
    def leidos():
        return render_template(
            "Botones superiores/leidos.html"
        )


    @app.route("/seguimiento")
    def seguimiento():
        return render_template(
            "seguimiento/seguimiento.html"
        )


    # -------------------------
    # AGREGAR LIBRO
    # -------------------------

    @app.route("/agregar")
    def agregar():
        return render_template(
            "agregar.html"
        )

    # -------------------------
    # FORMULUARIO REGISTRO
    # -------------------------

    @app.route("/formulario-principiante")
    def formulario_principiante():
        return render_template("HTML SESION/Formulario de principiante.html")

    @app.route("/formulario-intermedio")
    def formulario_intermedio():
        return render_template("HTML SESION/Formulario intermedio.html")

    @app.route("/formulario-experto")
    def formulario_experto():
        return render_template("HTML SESION/Formulario de experto.html")

    # -------------------------
    # FORMULUARIO REGISTRO GUARDADO
    # -------------------------

    @app.route("/api/guardar_encuesta", methods=["POST"])
    def guardar_encuesta():

        datos = request.json

        id_usuario = Preferencias.obtener_usuario_pendiente()

        if not id_usuario:

            return jsonify({
                "error": "No existe un usuario pendiente."
            }), 400

        preferencias = Preferencias(
            id_usuario=id_usuario,
            nivel=datos["nivel"],
            respuestas=datos["respuestas"]
        )

        preferencias.guardar()

        Preferencias.limpiar_usuario_pendiente(
            id_usuario
        )

        return jsonify({
            "mensaje": "Encuesta guardada correctamente."
        }), 200
