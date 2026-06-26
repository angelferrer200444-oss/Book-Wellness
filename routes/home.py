from flask import render_template, session
import db


def registrar_rutas(app):

    # -------------------------
    # PÁGINA PRINCIPAL
    # -------------------------

    @app.route("/")
    def home():

        libros_leyendo = []
        libros_pendientes = []

        id_usuario = session.get("id_usuario")

        if id_usuario:

            libros_leyendo = db.obtener_libros_usuario(
                id_usuario,
                "leyendo"
            )

            libros_pendientes = db.obtener_libros_usuario(
                id_usuario,
                "pendiente"
            )

        return render_template(
            "index.html",
            libros_leyendo=libros_leyendo,
            libros_pendientes=libros_pendientes
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
        return render_template(
            "Botones superiores/estadisticas.html"
        )


    @app.route("/objetivo")
    def objetivo():
        return render_template(
            "Botones superiores/objetivo.html"
        )


    @app.route("/notas")
    def notas():
        return render_template(
            "Botones superiores/notas.html"
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
