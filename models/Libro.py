from db import obtener_conexion

import Libros as libros_api
from GoogleLibros import GoogleBooksAPI

from routes.utilidades import obtener_json


class Libro:

    google_api = GoogleBooksAPI()
    openlibrary_api = libros_api.LibroAPI()

    def __init__(
        self,
        id_usuario=None,
        titulo=None,
        autor=None,
        descripcion=None,
        portada=None,
        categoria=None,
        key_libro=None,
        paginas=None,
        id_google=None,
        genero=None,
        anio=None,
        es_manual=False,
        formato=None
    ):
        self.id_usuario = id_usuario
        self.titulo = titulo
        self.autor = autor
        self.descripcion = descripcion
        self.portada = portada
        self.categoria = categoria
        self.key_libro = key_libro
        self.paginas = paginas
        self.id_google = id_google
        self.genero = genero
        self.anio = anio
        self.es_manual = es_manual
        self.formato = formato

    # ==========================
    # GUARDAR
    # ==========================

    def guardar(self):

        if (
            self.portada
            and isinstance(self.portada, str)
            and self.portada.startswith("http://")
        ):
            self.portada = self.portada.replace(
                "http://",
                "https://",
                1
            )

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id_libro
            FROM libros
            WHERE id_usuario = %s
            AND titulo = %s
        """, (
            self.id_usuario,
            self.titulo
        ))

        if cursor.fetchone():

            cursor.close()
            conexion.close()

            return False

        cursor.execute("""
            INSERT INTO libros
            (
                id_usuario,
                titulo,
                autor,
                descripcion,
                portada,
                categoria,
                key_libro,
                paginas_totales,
                id_google,
                genero,
                anio,
                es_agregado_manualmente,
                formato
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            self.id_usuario,
            self.titulo,
            self.autor,
            self.descripcion,
            self.portada,
            self.categoria,
            self.key_libro,
            self.paginas,
            self.id_google,
            self.genero,
            self.anio,
            self.es_manual,
            self.formato
        ))

        conexion.commit()

        id_nuevo = cursor.lastrowid

        cursor.close()
        conexion.close()

        return id_nuevo

    # ==========================
    # OBTENER
    # ==========================

    @staticmethod
    def obtener(id_libro):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM libros
            WHERE id_libro = %s
        """, (id_libro,))

        libro = cursor.fetchone()

        cursor.close()
        conexion.close()

        return libro

    @staticmethod
    def obtener_libros_usuario(
        id_usuario,
        categoria
    ):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_libro,
                titulo,
                autor,
                portada,
                key_libro,
                id_google,
                es_agregado_manualmente
            FROM libros
            WHERE id_usuario = %s
            AND categoria = %s
        """, (
            id_usuario,
            categoria
        ))

        libros = cursor.fetchall()

        cursor.close()
        conexion.close()

        return libros

    @staticmethod
    def eliminar(
        id_libro,
        id_usuario
    ):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            DELETE FROM libros
            WHERE id_libro = %s
            AND id_usuario = %s
        """, (
            id_libro,
            id_usuario
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar_datos(
        id_libro,
        paginas_totales=None,
        num_caps=None,
        formato=None
    ):

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        campos = []
        valores = []

        if paginas_totales is not None:
            campos.append("paginas_totales = %s")
            valores.append(paginas_totales)

        if num_caps is not None:
            campos.append("num_caps = %s")
            valores.append(num_caps)

        if formato is not None:
            campos.append("formato = %s")
            valores.append(formato)

        if campos:

            valores.append(id_libro)

            query = f"""
                UPDATE libros
                SET {', '.join(campos)}
                WHERE id_libro = %s
            """

            cursor.execute(query, valores)

            conexion.commit()

        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_completo(
        id_google=None,
        key_libro=None
    ):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        if id_google:

            cursor.execute("""
                SELECT *
                FROM libros
                WHERE id_google = %s
                LIMIT 1
            """, (id_google,))

        elif key_libro:

            cursor.execute("""
                SELECT *
                FROM libros
                WHERE key_libro = %s
                LIMIT 1
            """, (key_libro,))

        else:

            cursor.close()
            conexion.close()

            return None

        libro = cursor.fetchone()

        cursor.close()
        conexion.close()

        return libro

# ==========================
    # FORMATEAR RESPUESTA
    # ==========================

    @staticmethod
    def formatear_respuesta(libro):

        return {
            "titulo": libro.get(
                "titulo",
                "Sin título"
            ),
            "subtitulo": "",
            "descripcion": libro.get(
                "descripcion",
                "Descripción no disponible"
            ),
            "autor": libro.get(
                "autor",
                "Autor desconocido"
            ),
            "anio": libro.get(
                "anio",
                "Desconocido"
            ),
            "paginas": libro.get(
                "paginas_totales",
                "Desconocido"
            ),
            "generos": libro.get(
                "genero",
                "No disponible"
            ),
            "pais": "Desconocido",
            "formato": libro.get(
                "formato",
                "Desconocido"
            ),
            "portada": libro.get(
                "portada",
                ""
            )
        }

    # ==========================
    # GOOGLE BOOKS
    # ==========================

    @classmethod
    def buscar_google(
        cls,
        texto
    ):

        return cls.google_api.buscar_libros(texto)

    @classmethod
    def obtener_google(
        cls,
        id_google
    ):

        return cls.google_api.obtener_libro(
            id_google
        )

    # ==========================
    # OPENLIBRARY
    # ==========================

    @classmethod
    def buscar_openlibrary(
        cls,
        texto
    ):

        return cls.openlibrary_api.buscar_libros(
            texto
        )

    @classmethod
    def obtener_desde_bd_o_google(
        cls,
        id_libro=None,
        id_google=None,
        clave=None
    ):

        libro_bd = None

        if id_google:

            libro_bd = cls.obtener_completo(
                id_google=id_google
            )

        elif clave:

            libro_bd = cls.obtener_completo(
                key_libro=clave
            )

        if id_libro:

            libro_bd = cls.obtener(id_libro)

            if libro_bd:

                return cls.formatear_respuesta(
                    libro_bd
                )

        if libro_bd:

            return cls.formatear_respuesta(
                libro_bd
            )

        if id_google:

            try:

                return cls.obtener_google(
                    id_google
                )

            except Exception as e:

                print(
                    "Falló Google Books:",
                    e
                )

                print(
                    "Usando OpenLibrary como respaldo"
                )

        return None

    @classmethod
    def obtener_openlibrary(
        cls,
        clave,
        portada=""
    ):

        if not clave:

            return {
                "error": "Clave inválida"
            }

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

                return {
                    "error": (
                        "No fue posible obtener "
                        "la información"
                    )
                }

            try:
                titulo = datos.get(
                    "title",
                    titulo
                )
            except Exception:
                pass

            try:
                subtitulo = datos.get(
                    "subtitle"
                )
            except Exception:
                pass

            try:
                anio = datos.get(
                    "first_publish_date"
                )
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

                    ediciones = obtener_json(
                        url_ed
                    )

                    if ediciones:

                        for ed in ediciones.get(
                            "entries",
                            []
                        ):

                            if not subtitulo:

                                subtitulo = ed.get(
                                    "subtitle"
                                )

                            if not anio:

                                anio = (
                                    ed.get(
                                        "publish_date"
                                    )
                                    or (
                                        ed.get(
                                            "publish_year"
                                        )[0]
                                        if ed.get(
                                            "publish_year"
                                        )
                                        else None
                                    )
                                )

                            if paginas == "Desconocido":

                                paginas = (
                                    ed.get(
                                        "number_of_pages"
                                    )
                                    or paginas
                                )

                            if formato == "Físico":

                                formato = (
                                    ed.get(
                                        "physical_format"
                                    )
                                    or formato
                                )

                            if pais == "Desconocido":

                                lugares = ed.get(
                                    "publish_places",
                                    []
                                )

                                if lugares:

                                    if isinstance(
                                        lugares[0],
                                        dict
                                    ):
                                        pais = lugares[0].get(
                                            "name",
                                            "Desconocido"
                                        )

                                    else:

                                        pais = str(
                                            lugares[0]
                                        )

                            if (
                                subtitulo
                                and anio
                                and paginas != "Desconocido"
                                and pais != "Desconocido"
                            ):
                                break

                except Exception as e:

                    print(
                        "ERROR EDICIONES:",
                        e
                    )

            subtitulo = subtitulo or ""

            anio = (
                anio
                or "Desconocido"
            )

            try:

                if "description" in datos:

                    if isinstance(
                        datos["description"],
                        dict
                    ):

                        descripcion = (
                            datos["description"].get(
                                "value",
                                descripcion
                            )
                        )

                    else:

                        descripcion = (
                            datos["description"]
                        )

            except Exception:
                pass

            autores = []

            try:

                for a in datos.get(
                    "authors",
                    []
                ):

                    if (
                        isinstance(a, dict)
                        and "author" in a
                    ):

                        autor_key = (
                            a["author"].get(
                                "key"
                            )
                        )

                        if autor_key:

                            try:

                                datos_autor = (
                                    obtener_json(
                                        f"https://openlibrary.org{autor_key}.json"
                                    )
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

                autor = ", ".join(
                    autores
                )

            try:

                subjects = datos.get(
                    "subjects",
                    []
                )

                if subjects:

                    generos = ", ".join(
                        subjects[:5]
                    )

            except Exception:
                pass

            try:

                lugares = datos.get(
                    "subject_places",
                    []
                )

                if lugares:

                    pais = lugares[0]

            except Exception:
                pass

            try:

                formatos = datos.get(
                    "physical_format"
                )

                if formatos:

                    formato = formatos

            except Exception:
                pass

            return {

                "titulo": titulo,
                "subtitulo": subtitulo,
                "descripcion": descripcion,
                "autor": autor,
                "anio": anio,
                "paginas": paginas,
                "generos": generos,
                "pais": pais,
                "formato": formato,
                "portada": portada

            }

        except Exception as e:

            return {
                "error": str(e)
            }
