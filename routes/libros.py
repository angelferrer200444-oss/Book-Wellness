from flask import render_template, request, jsonify

import Libros as libros_api
from GoogleLibros import GoogleBooksAPI

from routes.utilidades import obtener_json


google_api = GoogleBooksAPI()
openlibrary_api = libros_api.LibroAPI()


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

            libros = google_api.buscar_libros(texto)

            if not libros:
                libros = openlibrary_api.buscar_libros(texto)

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

        # ===== GOOGLE BOOKS =====

        id_google = request.args.get("id")

        if id_google:

            try:

                libro = google_api.obtener_libro(id_google)

                return jsonify(libro)

            except Exception as e:

                print("Falló Google Books:", e)
                print("Usando OpenLibrary como respaldo")

        # ===== OPENLIBRARY =====

        clave = request.args.get("clave")

        if not clave:
            return jsonify({"error": "Clave inválida"}), 400

        titulo = "Sin título"
        subtitulo = ""
        descripcion = "Descripción no disponible"
        autor = "Autor desconocido"
        anio = "Desconocido"
        paginas = "Desconocido"
        generos = "No disponible"
        pais = "Desconocido"
        formato = "Físico"

        try:

            print("Voy a pedir datos")

            datos = obtener_json(
                f"https://openlibrary.org{clave}.json"
            )

            print("Datos recibidos")


            if not datos:

                print("Voy a devolver la respuesta")

                print(type(titulo), titulo)
                print(type(subtitulo), subtitulo)
                print(type(descripcion), descripcion)
                print(type(autor), autor)
                print(type(anio), anio)
                print(type(paginas), paginas)
                print(type(generos), generos)
                print(type(pais), pais)
                print(type(formato), formato)


                return jsonify({
                    "error": "No fue posible obtener la información"
                }), 500

            try:
                titulo = datos.get("title", titulo)
            except Exception:
                pass

            try:
                subtitulo = datos.get("subtitle")
            except Exception:
                pass

            try:
                anio = datos.get("first_publish_date")
            except Exception:
                pass


            if (
                not subtitulo
                or not anio
                or paginas == "Desconocido"
                or pais == "Desconocido"
                or formato == "Físico"
            ):

                try:

                    url_ed = (
                        f"https://openlibrary.org"
                        f"{clave}/editions.json?limit=20"
                    )

                    ediciones = obtener_json(url_ed)

                    if ediciones:

                        for ed in ediciones.get("entries", []):

                            if not subtitulo:
                                subtitulo = ed.get("subtitle")

                            if not anio:

                                anio = (
                                    ed.get("publish_date")
                                    or (
                                        ed.get("publish_year")[0]
                                        if ed.get("publish_year")
                                        else None
                                    )
                                )

                            if paginas == "Desconocido":

                                paginas = (
                                    ed.get("number_of_pages")
                                    or paginas
                                )

                            if formato == "Físico":

                                formato = (
                                    ed.get("physical_format")
                                    or formato
                                )

                            if pais == "Desconocido":

                                lugares = ed.get("publish_places", [])

                                if lugares:

                                    if isinstance(lugares[0], dict):
                                        pais = lugares[0].get(
                                            "name",
                                            "Desconocido"
                                        )

                                    else:
                                        pais = str(lugares[0])

                            if (
                                subtitulo
                                and anio
                                and paginas != "Desconocido"
                                and pais != "Desconocido"
                            ):
                                break


                except Exception as e:
                    print("ERROR AUTORES:", e)


            subtitulo = subtitulo or ""
            anio = anio or "Desconocido"

            try:

                if "description" in datos:

                    if isinstance(datos["description"], dict):

                        descripcion = datos["description"].get(
                            "value",
                            descripcion
                        )

                    else:

                        descripcion = datos["description"]

            except Exception:
                pass


            autores = []

            try:

                for a in datos.get("authors", []):

                    if isinstance(a, dict) and "author" in a:

                        autor_key = a["author"].get("key")

                        if autor_key:

                            try:

                                datos_autor = obtener_json(
                                    f"https://openlibrary.org{autor_key}.json"
                                )

                                if datos_autor:

                                    autores.append(
                                        datos_autor.get(
                                            "name",
                                            "Autor desconocido"
                                        )
                                    )

                            except Exception:
                                pass

            except Exception:
                pass

            if autores:

                autor = ", ".join(autores)


            try:

                subjects = datos.get("subjects", [])

                if subjects:
                    generos = ", ".join(subjects[:5])

            except Exception:
                pass


            try:

                lugares = datos.get("subject_places", [])

                if lugares:
                    pais = lugares[0]

            except Exception:
                pass


            try:

                formatos = datos.get("physical_format")

                if formatos:
                    formato = formatos

            except Exception:
                pass



            return jsonify({

                "titulo": titulo,
                "subtitulo": subtitulo,
                "descripcion": descripcion,
                "autor": autor,
                "anio": anio,

                "paginas": paginas,
                "generos": generos,
                "pais": pais,
                "formato": formato

            })

        except Exception as e:

            return jsonify({
                "error": str(e)
            }), 500

    # -------------------------
    # FILTRO POR GÉNERO
    # -------------------------

    @app.route("/filtrar")
    def filtrar():

        genero = request.args.get("genero", "")

        return render_template(
            "BusquedaDeLibros.html",
            consulta=genero
        )