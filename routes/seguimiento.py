from flask import render_template, request, jsonify, session
import db

# -------------------------
# ELIMINAR LIBRO
# -------------------------
def registrar_rutas(app):
    
    @app.route('/api/eliminar_libro', methods=['DELETE'])
    def eliminar_libro():

        datos = request.json
        print("DATOS RECIBIDOS:", datos)

        id_libro = datos.get('id_libro')
        id_usuario = datos.get('id_usuario')

        print("ID_LIBRO:", id_libro, "ID_USUARIO:", id_usuario)

        if not id_libro or not id_usuario:
            return jsonify({
                "error": "Datos incompletos"
            }), 400

        try:
            db.eliminar_libro(
                int(id_libro),
                int(id_usuario)
            )

            return jsonify({
                "mensaje": "Libro eliminado"
            }), 200

        except Exception as e:
            print("ERROR ELIMINAR:", str(e))
            return jsonify({
                "error": str(e)
            }), 500