from flask import render_template
from flask import request
from flask import session
from flask import jsonify
from models.Libro import Libro
from models.estadistica import Estadistica
from models.Preferencias import Preferencias
from IA.EstadoAnimo import EstadoAnimo
from models.Ob_Logros.logros import Logros

import db


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
            libros_leyendo = Libro.obtener_libros_usuario(id_usuario, "leyendo")
            libros_pendientes = Libro.obtener_libros_usuario(id_usuario, "pendiente")
            perfil = Estadistica.consultar(id_usuario)
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

        id_usuario = session.get("id_usuario")

        perfil = Estadistica.consultar(id_usuario) if id_usuario else None

        estado_actual = (
            EstadoAnimo.obtener_actual(id_usuario)
            if id_usuario else None
        )

        return render_template(
            "Botones superiores/estadisticas.html",
            perfil=perfil,
            estado_actual=estado_actual
        )

    @app.route("/api/logros")
    def obtener_logros():

        id_usuario = session.get("id_usuario")

        if not id_usuario:
            return jsonify({
                "error": "Usuario no autenticado."
            }), 401

        datos = Logros.obtener_logros(id_usuario)

        logros = []

        for grupo in datos.values():
            if isinstance(grupo, list):
                logros.extend(grupo)

        return jsonify(logros), 200





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

    @app.route("/api/estado_animo_actual", methods=["POST"])
    def guardar_estado_animo_actual():

        id_usuario = session.get("id_usuario")

        if not id_usuario:
            return jsonify({
                "error": "Usuario no autenticado."
            }), 401

        datos = request.json

        estado = datos.get("estado")

        print("Estado recibido:", estado)

        if not estado:
            return jsonify({
                "error": "No se recibió ningún estado de ánimo."
            }), 400

        EstadoAnimo.guardar(
            id_usuario,
            estado
        )

        mensaje = ""

        if estado.lower() == "feliz":
            mensaje = EstadoAnimo.responder_feliz(id_usuario)

        elif estado.lower() == "tranquilo":

            mensaje = EstadoAnimo.responder_tranquilo(
                id_usuario
            )
        
        elif estado == "Reflexivo":

            print("Entré a Reflexivo")

            resultado = EstadoAnimo.responder_reflexivo(
                id_usuario
            )

            print("RESULTADO:", resultado)
            print("RECOMENDACIONES:", resultado["recomendaciones"])
            print("CANTIDAD:", len(resultado["recomendaciones"]))

            return jsonify({

                "mensaje": "Estado guardado.",

                "respuesta_ia": resultado["respuesta"],

                "recomendaciones": resultado["recomendaciones"]

            })

        elif estado == "Sorprendido":

            print("Entré a Sorprendido")

            resultado = EstadoAnimo.responder_sorprendido(
                id_usuario
            )

            return jsonify({

                "mensaje": "Estado guardado.",

                "respuesta_ia": resultado["respuesta"],

                "recomendaciones": resultado["recomendaciones"]

            })
        
        elif estado.lower() == "ansioso":

            resultado = EstadoAnimo.responder_ansioso(
                id_usuario
            )

            return jsonify({

                "mensaje": "Estado guardado.",

                "respuesta_ia": resultado["respuesta"],

                "recomendaciones": resultado["recomendaciones"]

            })





        print("Respuesta IA:", mensaje)
        
        return jsonify({
            "mensaje": "Estado de ánimo guardado correctamente.",
            "respuesta_ia": mensaje
        }), 200
