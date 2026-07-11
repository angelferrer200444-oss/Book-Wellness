from flask import render_template, request, jsonify, session
import db

import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name = "jklaybsr",
    api_key = "",
    api_secret = ""  
)
# -------------------------
# ELIMINAR LIBRO
# -------------------------
def registrar_rutas(app):

    @app.route('/api/agregar_libro_manual', methods=['POST'])
    def agregar_libro_manual():
        id_usuario = session.get('id_usuario')
        
        if not id_usuario:
            return jsonify({"error": "No hay sesión activa"}), 401

        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        descripcion = request.form.get('descripcion', '')
        paginas = request.form.get('paginas')
        capitulos = request.form.get('capitulos')
        anio = request.form.get('anio')
        genero = request.form.get('genero')
        formato = request.form.get('formato')
        categoria = request.form.get('categoria', 'pendiente')

        if not titulo or not autor:
            return jsonify({"error": "Título y autor son obligatorios"}), 400

        portada = None
        if 'portada' in request.files:
            archivo = request.files['portada']
            if archivo.filename != '':
                try:
                    resultado_cloud = cloudinary.uploader.upload(archivo)
                    portada = resultado_cloud.get('secure_url')
                except Exception as e:
                    print("ERROR CLOUDINARY:", e)

        try:
                    resultado = db.agregar_libro(
                        id_usuario, titulo, autor, descripcion, portada,
                        categoria, None, paginas, None, genero, anio, True, formato
                    )

                    if resultado:
                        if capitulos:
                        
                            db.actualizar_datos_libro(resultado, num_caps=int(capitulos))
                        db.invalidar_cache_recomendaciones(id_usuario)
                        return jsonify({"mensaje": "Libro agregado correctamente"}), 201
                    return jsonify({"error": "Este libro ya está en tu lista"}), 409

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    
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
            db.invalidar_cache_recomendaciones(id_usuario)

            return jsonify({
                "mensaje": "Libro eliminado"
            }), 200

        except Exception as e:
            print("ERROR ELIMINAR:", str(e))
            return jsonify({
                "error": str(e)
            }), 500
        


