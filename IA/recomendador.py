import json
import requests

from GoogleLibros import GoogleBooksAPI
import db

from flask import Blueprint
from flask import jsonify
from flask import session

API_KEY = "LA KEY NO SE PUBLICA"

PROMPT_RECOMENDADOR = """
Eres un experto en literatura.

Recibirás un diccionario con los géneros favoritos de un lector.

Tu tarea es recomendar exactamente cinco libros.

Reglas:

- Devuelve únicamente JSON.
- No escribas explicaciones.
- No escribas introducciones.
- No escribas markdown.
- No repitas libros.
- Los libros deben existir realmente.

Formato EXACTO:

[
    {
        "titulo":"...",
        "autor":"..."
    }
]
"""


class RecomendadorLibros:

    def __init__(self, api_key):

        self.api_key = api_key

        self.google = GoogleBooksAPI()

        self.google.__init__()

        self.url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.5-flash:generateContent"
        )

    ##########################################################
    # OBTENER GÉNEROS DEL USUARIO
    ##########################################################

    def obtener_generos(self, id_usuario):

        conexion = db.obtener_conexion()

        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT genero
            FROM libros
            WHERE id_usuario=%s
            """,
            (id_usuario,)
        )

        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        contador = {}

        for fila in filas:

            if not fila[0]:
                continue

            lista = fila[0].split(",")

            for genero in lista:

                genero = genero.strip()

                if genero == "":
                    continue

                contador[genero] = contador.get(genero, 0) + 1

        return contador

    ##########################################################
    # CONSTRUIR EL PROMPT
    ##########################################################

    def construir_prompt(self, generos):

        texto = PROMPT_RECOMENDADOR

        texto += "\n\n"

        texto += "Géneros favoritos del usuario:\n\n"

        for genero, cantidad in sorted(
            generos.items(),
            key=lambda x: x[1],
            reverse=True
        ):

            texto += f"- {genero}: {cantidad} libros\n"

        return texto

    ##########################################################
    # CONSULTAR GEMINI
    ##########################################################

    def consultar_gemini(self, prompt):

        body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        respuesta = requests.post(

            self.url,

            params={
                "key": self.api_key
            },

            json=body,

            timeout=20

        )

        respuesta.raise_for_status()

        datos = respuesta.json()

        texto = (
            datos["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

        texto = texto.replace("```json", "")
        texto = texto.replace("```", "")
        texto = texto.strip()

        return json.loads(texto)

##########################################################
    # BUSCAR LIBROS EN GOOGLE BOOKS
    ##########################################################

    def buscar_libros(self, recomendaciones):

        libros = []

        for recomendacion in recomendaciones:

            titulo = recomendacion.get("titulo", "")
            autor = recomendacion.get("autor", "")

            consulta = f"{titulo} {autor}"

            resultados = self.google.buscar_libros(consulta)

            if len(resultados) == 0:
                continue

            libro = resultados[0]

            libros.append({

                "titulo": libro["titulo"],

                "autor": libro["autor"],

                "descripcion": libro["descripcion"],

                "portada": libro["portada"],

                "paginas": libro["paginas"],

                "generos": libro["generos"],

                "anio": libro["anio"],

                "id_google": libro["id_google"]

            })

        return libros

    ##########################################################
    # RECOMENDACIONES POR DEFECTO
    ##########################################################

    def recomendaciones_defecto(self):

        recomendaciones = [

            {
                "titulo": "El Hobbit",
                "autor": "J. R. R. Tolkien"
            },

            {
                "titulo": "1984",
                "autor": "George Orwell"
            },

            {
                "titulo": "Orgullo y prejuicio",
                "autor": "Jane Austen"
            },

            {
                "titulo": "Cien años de soledad",
                "autor": "Gabriel García Márquez"
            },

            {
                "titulo": "Los juegos del hambre",
                "autor": "Suzanne Collins"
            }

        ]

        return self.buscar_libros(recomendaciones)

    ##########################################################
    # MÉTODO PRINCIPAL
    ##########################################################

    def recomendar(self, id_usuario):

        generos = self.obtener_generos(id_usuario)

        if len(generos) == 0:

            return self.recomendaciones_defecto()

        prompt = self.construir_prompt(generos)

        try:

            recomendaciones = self.consultar_gemini(prompt)

        except Exception as e:

            print("=" * 60)
            print("ERROR GEMINI")
            print(e)
            print("=" * 60)

            return self.recomendaciones_defecto()

        libros = self.buscar_libros(recomendaciones)

        if len(libros) == 0:

            return self.recomendaciones_defecto()

        return libros

recomendador_bp = Blueprint(
    "recomendador",
    __name__
)

motor = RecomendadorLibros(API_KEY)

@recomendador_bp.route(
    "/api/recomendaciones",
    methods=["GET"]
)

def recomendaciones():

    if "id_usuario" not in session:

        return jsonify([])

    id_usuario = session["id_usuario"]

    try:

        libros = motor.recomendar(id_usuario)

        return jsonify(libros)

    except Exception as e:

        print("=" * 60)
        print("ERROR RECOMENDADOR")
        print(e)
        print("=" * 60)

        return jsonify([])



