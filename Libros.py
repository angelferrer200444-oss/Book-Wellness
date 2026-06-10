import random
import requests

class LibroAPI:

    def __init__(self):
        self.url_base = "https://openlibrary.org/search.json"

    def obtener_portada(self, libro):

        editions = libro.get("edition_key", [])
        isbns = libro.get("isbn", [])
        cover_id = libro.get("cover_i")

        if editions:
            return f"https://covers.openlibrary.org/b/olid/{editions[0]}-L.jpg"

        if isbns:
            return f"https://covers.openlibrary.org/b/isbn/{isbns[0]}-L.jpg"

        if cover_id:
            return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

        return "https://via.placeholder.com/200x300?text=Sin+Portada"

    def buscar_libros(self, texto):

        if not texto:
            return []

        try:

            respuesta = requests.get(
                self.url_base,
                params={"q": texto},
                timeout=10
            )

            respuesta.raise_for_status()

            datos = respuesta.json()

            todos_los_libros = datos.get("docs", [])

            if len(todos_los_libros) > 20:

                libros_aleatorios = random.sample(
                    todos_los_libros,
                    20
                )

            else:

                libros_aleatorios = todos_los_libros

            libros = []

            for libro in libros_aleatorios:
               

                libros.append({

                    "titulo": libro.get(
                        "title",
                        "Sin título"
                    ),

                    "autor": ", ".join(
                        libro.get(
                            "author_name",
                            ["Autor desconocido"]
                        )
                    ),

                    "anio": libro.get(
                        "first_publish_year",
                        "Desconocido"
                    ),

                    "portada": self.obtener_portada(libro),

                    "idiomas": libro.get(
                        "language",
                        []
                    ),

                    "key": libro.get(
                        "key",
                        ""
                    )

                })

            return libros

        except requests.exceptions.RequestException as e:

            print("Error API:", e)

            return []
