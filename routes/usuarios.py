from flask import request, jsonify, session
import db


def registrar_rutas(app):

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

            return jsonify({
                "error": "Credenciales incorrectas"
            }), 401


    @app.route('/api/logout', methods=['POST'])
    def logout():

        session.clear()

        return jsonify({
            "mensaje": "Sesión cerrada"
        }), 200
