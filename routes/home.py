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

            orden = request.args.get("orden")

            libros_leyendo = Libro.obtener_libros_usuario(
                id_usuario,
                "leyendo",
                orden
            )

            libros_pendientes = Libro.obtener_libros_usuario(
                id_usuario,
                "pendiente",
                orden
            )

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
        id_usuario = session.get('id_usuario')
        leidos = Libro.obtener_libros_usuario(id_usuario, 'leido') if id_usuario else []
        inconclusos = Libro.obtener_libros_usuario(id_usuario, 'inconcluso') if id_usuario else []
        audiolibros = Libro.obtener_libros_usuario_formato(id_usuario, 'Audiolibro') if id_usuario else []
        return render_template(
            "Botones superiores/Leidos.html",
            leidos=leidos,
            inconclusos=inconclusos,
            audiolibros=audiolibros
        )
        
    @app.route('/api/reanudar_libro', methods=['POST'])
    def reanudar_libro():
        from flask import request, jsonify, session
        from models.Libro import Libro
        id_usuario = session.get('id_usuario')
        if not id_usuario:
            return jsonify({"error": "No hay sesión"}), 401
        datos = request.json
        Libro.actualizar_categoria(datos.get('id_libro'), 'leyendo')
        return jsonify({"mensaje": "Libro reanudado"}), 200


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

        # ==========================================
        # COMPROBAR LAS 24 HORAS
        # ==========================================

        conexion = db.obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT fecha_hora
            FROM estado_animo_actual
            WHERE id_usuario = %s
            ORDER BY fecha_hora DESC
            LIMIT 1
        """, (id_usuario,))

        ultimo_estado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if ultimo_estado:

            from datetime import datetime, timedelta

            fecha_ultimo = ultimo_estado["fecha_hora"]
            ahora = datetime.now()

            diferencia = ahora - fecha_ultimo

            if diferencia < timedelta(hours=24):

                horas_restantes = 24 - (
                    diferencia.total_seconds() / 3600
                )

                return jsonify({
                    "error": "Ya registraste un estado de ánimo recientemente.",
                    "bloqueado": True,
                    "horas_restantes": round(horas_restantes, 1)
                }), 429

        # ==========================================
        # GUARDAR ESTADO
        # ==========================================

        EstadoAnimo.guardar(
            id_usuario,
            estado
        )

        mensaje = ""

        if estado.lower() == "feliz":

            mensaje = EstadoAnimo.responder_feliz(
                id_usuario
            )

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
            print(
                "RECOMENDACIONES:",
                resultado["recomendaciones"]
            )
            print(
                "CANTIDAD:",
                len(resultado["recomendaciones"])
            )

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

        elif estado == "Triste":

            resultado = EstadoAnimo.responder_triste(
                id_usuario
            )

            return jsonify({
                "mensaje": "Estado guardado.",
                "respuesta_ia": resultado["respuesta"],
                "recomendaciones": resultado.get(
                    "recomendaciones",
                    []
                )
            }), 200

        return jsonify({
            "mensaje": "Estado de ánimo guardado correctamente.",
            "respuesta_ia": mensaje
        }), 200

    @app.route("/api/estado_animo_actual", methods=["GET"])
    def obtener_estado_animo_actual():

        id_usuario = session.get("id_usuario")

        if not id_usuario:
            return jsonify({
                "estado": None
            }), 401

        conexion = db.obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT estado_animo, fecha_hora
            FROM estado_animo_actual
            WHERE id_usuario = %s
            ORDER BY fecha_hora DESC
            LIMIT 1
        """, (id_usuario,))

        ultimo_estado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if not ultimo_estado:
            return jsonify({
                "estado": None
            }), 200

        from datetime import datetime, timedelta

        fecha_ultimo = ultimo_estado["fecha_hora"]
        ahora = datetime.now()

        diferencia = ahora - fecha_ultimo

        if diferencia >= timedelta(hours=24):
            return jsonify({
                "estado": None
            }), 200

        return jsonify({
            "estado": ultimo_estado["estado_animo"]
        }), 200

    @app.route(
        "/api/triste/analizar",
        methods=["POST"]
    )
    def analizar_triste():

        if "id_usuario" not in session:

            return jsonify({
                "error": "Usuario no autenticado"
            }), 401

        datos = request.get_json()

        respuesta_usuario = datos.get(
            "respuesta",
            ""
        ).strip()

        if not respuesta_usuario:

            return jsonify({
                "error": "La respuesta está vacía."
            }), 400

        id_usuario = session["id_usuario"]

        resultado = EstadoAnimo.procesar_triste(
            id_usuario,
            respuesta_usuario
        )

        return jsonify({
            "respuesta_ia": resultado["respuesta"],
            "recomendaciones": resultado["recomendaciones"],
            "estado_triste": resultado["estado_triste"]
        }), 200

    @app.route("/historial-animo")
    def historial_animo():

        id_usuario = session.get("id_usuario")

        estados_animo = []

        if id_usuario:

            conexion = db.obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    estado_animo,
                    fecha_hora
                FROM estado_animo_actual
                WHERE id_usuario = %s
                ORDER BY fecha_hora DESC
            """, (id_usuario,))

            estados_animo = cursor.fetchall()

            cursor.close()
            conexion.close()

        return render_template(
            "Botones superiores/historial_animo.html",
            estados_animo=estados_animo
        )

    


    
