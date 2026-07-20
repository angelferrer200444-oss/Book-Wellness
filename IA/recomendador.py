import json
import requests
from flask import Blueprint, jsonify, session, request

from GoogleLibros import GoogleBooksAPI
import Libros as libros_api

import db

from flask import Blueprint
from flask import jsonify
from flask import session

API_KEY = ""

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
- No recomiendes ningún libro que aparezca en la lista "Libros que ya posee o ha leído el usuario".
- Si un libro ya fue leído por el usuario, elige otro.
- Verifica cuidadosamente la lista antes de generar las cinco recomendaciones.

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

        self.openlibrary = libros_api.LibroAPI()

        self.openlibrary.url_base = "https://openlibrary.org/search.json"



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
    # OBTENER TÍTULOS DEL USUARIO
    ##########################################################

    def obtener_titulos(self, id_usuario):

        conexion = db.obtener_conexion()

        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT titulo
            FROM libros
            WHERE id_usuario = %s
            """,
            (id_usuario,)
        )

        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        titulos = []

        for fila in filas:

            if fila[0]:

                titulos.append(fila[0].strip())

        return titulos

    ##########################################################
    # CONSTRUIR EL PROMPT
    ##########################################################

    def construir_prompt(self, generos, titulos):

        texto = PROMPT_RECOMENDADOR

        texto += "\n\n"

        texto += "Libros que ya posee o ha leído el usuario:\n\n"

        for titulo in titulos:

            texto += f"- {titulo}\n"

        texto += "\n"

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

                print("Google Books no encontró resultados.")
                print("Buscando en OpenLibrary...")

                resultados = self.openlibrary.buscar_libros(consulta)

            if len(resultados) == 0:
                continue

            libro = None

            for resultado in resultados:

                portada = resultado.get("portada", "")

                if portada and portada.strip():

                    libro = resultado
                    break

            if libro is None:
                continue


            libros.append({

                "titulo": libro["titulo"],

                "autor": libro["autor"],

                "descripcion": libro.get("descripcion", ""),

                "portada": libro["portada"],

                "paginas": libro.get("paginas", "Desconocido"),

                "generos": libro.get("generos", ""),

                "anio": libro["anio"],

                "id_google": libro.get("id_google", ""),

                "key": libro.get("key", "")

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

        print("=" * 60)
        print("INICIANDO RECOMENDADOR")
        print(f"Usuario: {id_usuario}")


        generos = self.obtener_generos(id_usuario)

        print("\nGÉNEROS DEL USUARIO:")

        for genero, cantidad in generos.items():
            print(f"- {genero}: {cantidad}")

        titulos = self.obtener_titulos(id_usuario)

        print("\nLIBROS DEL USUARIO:")

        for titulo in titulos:
            print(f"- {titulo}")

        if len(generos) == 0:

            return self.recomendaciones_defecto()

        prompt = self.construir_prompt(generos, titulos)

        print("\nENVIANDO PROMPT A GEMINI...")
        print("-" * 60)
        print(prompt)
        print("-" * 60)

        try:

            recomendaciones = self.consultar_gemini(prompt)

            print("\nRESPUESTA DE GEMINI:")

            for libro in recomendaciones:
                print(f"- {libro['titulo']} | {libro['autor']}")

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

    forzar = request.args.get('forzar', 'false') == 'true'
    if not forzar:
        cache = db.obtener_recomendaciones_cache(id_usuario)
        if cache:
            return jsonify(cache)

    

    try:

        libros = motor.recomendar(id_usuario)
        db.guardar_recomendaciones(id_usuario, libros)

        return jsonify(libros)

    except Exception as e:

        print("=" * 60)
        print("ERROR RECOMENDADOR")
        print(e)
        print("=" * 60)

        return jsonify([])
