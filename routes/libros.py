from flask import render_template, request, jsonify

from models.Libro import Libro


def registrar_rutas(app):

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

            libros = Libro.buscar_google(texto)

            if not libros:
                libros = Libro.buscar_openlibrary(texto)

            return jsonify(libros)

        except Exception as e:

            return jsonify({
                "error": str(e)
            }), 500


    # -------------------------
    # DETALLE LIBRO
    # -------------------------

    @app.route("/libro")
    def libro():

        clave = request.args.get("clave")
        portada = request.args.get("portada")
        id_google = request.args.get("id_google")

        return render_template(
            "libros.html",
            clave=clave,
            portada=portada,
            id_google=id_google
        )


    @app.route("/api/libro")
    def api_libro():

        print("Entró a api_libro")

        id_libro = request.args.get("id_libro")
        id_google = request.args.get("id")
        clave = request.args.get("clave")

        libro_bd = None

        if id_google:

            libro_bd = Libro.obtener_completo(
                id_google=id_google
            )

        elif clave:

            libro_bd = Libro.obtener_completo(
                key_libro=clave
            )

        if id_libro:

            libro_bd = Libro.obtener(id_libro)

            if libro_bd:

                return jsonify(
                    Libro.formatear_respuesta(
                        libro_bd
                    )
                )

        if libro_bd:

            return jsonify(
                Libro.formatear_respuesta(
                    libro_bd
                )
            )

        if id_google:

            try:

                return jsonify(
                    Libro.obtener_google(
                        id_google
                    )
                )

            except Exception as e:

                print(
                    "Falló Google Books:",
                    e
                )

                print(
                    "Usando OpenLibrary como respaldo"
                )

        return jsonify(
            Libro.obtener_openlibrary(
                clave,
                request.args.get(
                    "portada",
                    ""
                )
            )
        )


    @app.route("/libro-manual")
    def libro_manual():

        id_libro = request.args.get(
            "id_libro"
        )

        libro = None

        if id_libro:

            libro = Libro.obtener(
                id_libro
            )

        return render_template(
            "libros.html",
            clave=None,
            portada=(
                libro.get("portada")
                if libro else None
            ),
            id_google=None,
            id_libro=id_libro,
            libro_manual=libro
        )


    # -------------------------
    # FILTRO POR GÉNERO
    # -------------------------

    @app.route("/filtrar")
    def filtrar():

        genero = request.args.get(
            "genero",
            ""
        )

        return render_template(
            "BusquedaDeLibros.html",
            consulta=genero
        )
