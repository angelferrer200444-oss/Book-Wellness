import requests

class GoogleBooksAPI:

    def __init__(self):
        self.url_base = "https://www.googleapis.com/books/v1/volumes"
        self.api_key = "LA KEY NO SE PUEDE PUBLICAR"


    def buscar_libros(self, texto):

        if not texto:
            return []

        try:

            respuesta = requests.get(
                self.url_base,
                params={
                    "q": texto,
                    "maxResults": 20,
                    "key": self.api_key
                },
                timeout=5
            )

            respuesta.raise_for_status()

            datos = respuesta.json()

            resultados = []

            for item in datos.get("items", []):

                info = item.get("volumeInfo", {})

                imagen = (
                    info.get("imageLinks", {})
                    .get("thumbnail",
                         "https://via.placeholder.com/200x300?text=Sin+Portada")
                )

                resultados.append({

                    "titulo": info.get(
                        "title",
                        "Sin título"
                    ),

                    "subtitulo": info.get(
                        "subtitle",
                        ""
                    ),

                    "autor": ", ".join(
                        info.get(
                            "authors",
                            ["Autor desconocido"]
                        )
                    ),

                    "descripcion": info.get(
                        "description",
                        "Descripción no disponible"
                    ),

                    "paginas": info.get(
                        "pageCount",
                        "Desconocido"
                    ),

                    "generos": ", ".join(
                        info.get(
                            "categories",
                            []
                        )
                    ),

                    "anio": info.get(
                        "publishedDate",
                        "Desconocido"
                    ),

                    "pais": info.get(
                        "country",
                        "Desconocido"
                    ),

                    "formato": info.get(
                        "printType",
                        "BOOK"
                    ),

                    "portada": imagen,

                    "id_google": item.get(
                        "id",
                        ""
                    )

                })

            return resultados

        except Exception as e:

            print("="*50)
            print("ERROR GOOGLE BOOKS")
            print(e)
            print("="*50)

            return []


    def obtener_libro(self, id_google):

        respuesta = requests.get(
            f"{self.url_base}/{id_google}",
            params={
                "key": self.api_key
            }
        )

        datos = respuesta.json()

        info = datos["volumeInfo"]

        imagen = info.get(
            "imageLinks",
            {}
        ).get(
            "thumbnail",
            "https://via.placeholder.com/200x300?text=Sin+Portada"
        )

        return {

            "titulo": info.get("title", "Sin título"),

            "subtitulo": info.get("subtitle", ""),

            "autor": ", ".join(
                info.get(
                    "authors",
                    ["Autor desconocido"]
                )
            ),

            "descripcion": info.get(
                "description",
                "Descripción no disponible"
            ),

            "paginas": info.get(
                "pageCount",
                "Desconocido"
            ),

            "generos": ", ".join(
                info.get(
                    "categories",
                    []
                )
            ),

            "anio": info.get(
                "publishedDate",
                "Desconocido"
            ),

            "formato": info.get(
                "printType",
                "BOOK"
            ),

            "portada": imagen
        }

            

