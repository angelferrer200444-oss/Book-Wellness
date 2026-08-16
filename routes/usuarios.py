from flask import request, jsonify, session

import mysql.connector

from models.Usuario import Usuario
from IA.RecomendadorInicial import RecomendacionInicial


def registrar_rutas(app):

    # -------------------------
    # API USUARIOS
    # -------------------------

    @app.route("/api/registrar_usuario", methods=["POST"])
    def registrar_usuario():

        try:

            datos = request.json

            nombre_usuario = datos.get("nombre")
            correo_usuario = datos.get("correo")
            password_usuario = datos.get("password")
            nivel_usuario = datos.get("nivel")

            if not nombre_usuario or not correo_usuario or not password_usuario or not nivel_usuario:
                return jsonify({
                    "error": "Todos los campos son obligatorios"
                }), 400

            usuario = Usuario(
                nombre=nombre_usuario,
                correo=correo_usuario,
                password=password_usuario,
                nivel_actual=nivel_usuario
            )

            id_generado = usuario.registrar()

            return jsonify({
                "mensaje": f"¡Usuario {nombre_usuario} registrado con éxito!",
                "id_asignado": id_generado
            }), 201

        except mysql.connector.errors.IntegrityError:

            return jsonify({
                "error": "Este correo ya está registrado"
            }), 409

        except mysql.connector.Error as err:

            return jsonify({
                "error": f"Error en MySQL: {err.msg}"
            }), 500

        except Exception as e:

            return jsonify({
                "error": f"Error inesperado: {str(e)}"
            }), 500


    @app.route("/api/login", methods=["POST"])
    def login_usuario():

        datos = request.json

        correo = datos.get("correo")
        password = datos.get("password")

        if not correo or not password:
            return jsonify({
                "error": "Rellena todos los campos"
            }), 400

        usuario = Usuario.iniciar_sesion(
            correo,
            password
        )

        if usuario:

            session["id_usuario"] = usuario.id_usuario
            session["nombre"] = usuario.nombre

            return jsonify({
                "mensaje": f"¡Bienvenido, {usuario.nombre}!",
                "usuario": {
                    "id_usuario": usuario.id_usuario,
                    "nombre": usuario.nombre,
                    "correo": usuario.correo
                }
            }), 200



        return jsonify({
            "error": "Credenciales incorrectas"
        }), 401

    @app.route("/api/recomendacion-inicial", methods=["POST"])
    def recomendacion_inicial():

        id_usuario = session.get("id_usuario")

        if not id_usuario:
            return jsonify({
                "error": "Usuario no autenticado"
            }), 401

        if RecomendacionInicial.ya_generada(id_usuario):
            return jsonify({
                "mensaje": "La recomendación inicial ya fue generada."
            }), 200

        exito = RecomendacionInicial.generar(id_usuario)

        if not exito:
            return jsonify({
                "error": "No se pudo generar la recomendación inicial."
            }), 500

        return jsonify({
            "mensaje": "Recomendación inicial generada correctamente."
        }), 200


    @app.route("/api/logout", methods=["POST"])
    def logout():

        session.clear()

        return jsonify({
            "mensaje": "Sesión cerrada"
        }), 200
