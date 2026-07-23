from flask import app, render_template, request, jsonify, session
import db

def registrar_rutas(app):

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
        id_google = datos.get('id_google')
        genero = datos.get('genero')
        anio = datos.get('anio')

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
                paginas,
                id_google,
                genero,
                anio
            )

            if resultado:
                db.invalidar_cache_recomendaciones(id_usuario)

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

                lectura = db.obtener_lectura_en_progreso(
                    id_usuario,
                    id_libro
                )

                if lectura:

                    pagina_actual = lectura['pagina_actual']
                    capitulos_leidos = lectura['capitulos_leidos']
                    fecha_inicio = lectura['fecha_inicio']
                    fecha_fin = lectura['fecha_fin']
                    fecha_limite = lectura['fecha_limite']

        datos_completos = (
            libro and
            libro.get('paginas_totales') and
            libro.get('num_caps')
        )

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
    
    @app.route('/api/actualizar_progreso', methods=['POST'])
    def actualizar_progreso():
        datos = request.json
        id_usuario = session.get('id_usuario')
        id_libro = datos.get('id_libro')
        pagina_actual = datos.get('pagina_actual')
        capitulos_leidos = datos.get('capitulos_leidos')
        fecha_inicio = datos.get('fecha_inicio')

        if not id_usuario:
            return jsonify({"error": "No hay sesión activa"}), 401

        try:
            db.actualizar_progreso_lectura(id_usuario, id_libro, pagina_actual, capitulos_leidos, fecha_inicio)
            return jsonify({"mensaje": "Progreso actualizado"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        



    @app.route('/api/iniciar_lectura', methods=['POST'])
    def iniciar_lectura():

        datos = request.json

        id_libro = datos.get('id_libro')
        paginas_totales = datos.get('paginas_totales')
        num_caps = datos.get('num_caps')
        formato = datos.get('formato')

        try:

            db.actualizar_datos_libro(
                id_libro,
                paginas_totales,
                num_caps,
                formato
            )

            return jsonify({
                "mensaje": "Datos guardados"
            }), 200

        except Exception as e:

            return jsonify({
                "error": str(e)
            }), 500


    @app.route('/api/guardar_fecha_limite', methods=['POST'])
    def guardar_fecha_limite_ruta():

        datos = request.json

        id_usuario = session.get('id_usuario')
        id_libro = datos.get('id_libro')
        fecha_limite = datos.get('fecha_limite')

        if not id_usuario:
            return jsonify({
                "error": "No hay sesión activa"
            }), 401

        try:

            db.guardar_fecha_limite(
                id_usuario,
                id_libro,
                fecha_limite
            )

            return jsonify({
                "mensaje": "Fecha límite guardada"
            }), 200

        except Exception as e:

            return jsonify({
                "error": str(e)
            }), 500
        
    @app.route('/api/fechas_calendario')
    def fechas_calendario():
        id_usuario = session.get('id_usuario')
        if not id_usuario:
            return jsonify({}), 401
        fechas = db.obtener_fechas_calendario(id_usuario)
        return jsonify(fechas)


    @app.route('/api/libros_por_fecha')
    def libros_por_fecha():
        id_usuario = session.get('id_usuario')
        fecha = request.args.get('fecha')
        if not id_usuario or not fecha:
            return jsonify([]), 400
        libros = db.obtener_libros_por_fecha(id_usuario, fecha)
        return jsonify(libros)



    @app.route("/seccion2-lectura")
    def seccion2_lectura():

        id_libro = request.args.get('id_libro')

        libro = None

        if id_libro:
            libro = db.obtener_libro(id_libro)

        return render_template(
            "seccion-lectura/seccion2-lectura.html",
            libro=libro
        )


    @app.route('/seccion3-lectura')
    def seccion3_lectura():

        id_libro = request.args.get('id_libro')
        id_usuario = session.get('id_usuario')

        lectura = None

        if id_libro and id_usuario:

            lectura = db.obtener_lectura_en_progreso(
                id_usuario,
                id_libro
            )

        pagina_anterior = (
            lectura['pagina_actual']
            if lectura else 0
        )

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
            return jsonify({
                "error": "No hay sesión activa"
            }), 401

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

            # Guardar la reflexión únicamente si llegó información
            if (
                datos.get("estado_animo") or
                datos.get("notas") or
                datos.get("tipo_reflexion") or
                datos.get("respuesta_reflexion")
            ):

                db.guardar_notas_lectura(
                    id_lectura=id_lectura,
                    como_te_sientes=datos.get("estado_animo"),
                    continuara=datos.get("estado"),
                    notas=datos.get("notas"),
                    tipo_reflexion=datos.get("tipo_reflexion"),
                    respuesta_reflexion=datos.get("respuesta_reflexion")
                )

            return jsonify({
                "mensaje": "Lectura guardada"
            }), 201

        except Exception as e:

            return jsonify({
                "error": str(e)
            }), 500

    @app.route("/notas")
    def notas():
        id_usuario = session.get('id_usuario')
        notas_manuales, notas_sesion = db.obtener_notas_usuario(id_usuario) if id_usuario else ([], [])
        libros_leyendo = db.obtener_libros_usuario(id_usuario, 'leyendo') if id_usuario else []
        return render_template(
            "Botones superiores/notas.html",
            notas_manuales=notas_manuales,
            notas_sesion=notas_sesion,
            libros_leyendo=libros_leyendo
        )

    @app.route('/api/agregar_nota', methods=['POST'])
    def agregar_nota():
        id_usuario = session.get('id_usuario')
        if not id_usuario:
            return jsonify({"error": "No hay sesión"}), 401
        datos = request.json
        id_nueva = db.agregar_nota_usuario(
            id_usuario,
            datos.get('id_libro'),
            datos.get('titulo'),
            datos.get('contenido'),
            datos.get('categoria')
        )
        return jsonify({"id_nota": id_nueva}), 201

    @app.route('/api/editar_nota', methods=['POST'])
    def editar_nota():
        datos = request.json
        tipo = datos.get('tipo')
        if tipo == 'manual':
            db.editar_nota_usuario(datos.get('id_nota'), datos.get('titulo'), datos.get('contenido'), datos.get('categoria'))
        elif tipo == 'sesion':
            db.editar_nota_sesion(datos.get('id_nota'), datos.get('campo'), datos.get('valor'))
        return jsonify({"mensaje": "Nota actualizada"}), 200

    @app.route('/api/eliminar_nota', methods=['DELETE'])
    def eliminar_nota():
        datos = request.json
        tipo = datos.get('tipo')
        if tipo == 'manual':
            db.eliminar_nota_usuario(datos.get('id_nota'))
        return jsonify({"mensaje": "Nota eliminada"}), 200
