import json
import requests
from flask import Blueprint, jsonify, session, request
from .orquestador import OrquestadorIA

from GoogleLibros import GoogleBooksAPI
import Libros as libros_api

import db

from flask import Blueprint
from flask import jsonify
from flask import session

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
- El campo "mensaje" debe estar en español.
- Menciona los cinco libros recomendados.
- No inventes libros distintos a los que aparecen en "libros".
- Termina invitando al usuario a preguntar sobre cualquiera de ellos.

Formato EXACTO:

{
    "mensaje":"Escribe un mensaje natural dirigido al usuario. Menciona los cinco libros recomendados como una lista. Finaliza invitándolo a preguntarte sobre cualquiera de ellos si desea saber más.",

    "libros":[
        {
            "titulo":"...",
            "autor":"..."
        }
    ]
}



"""

PROMPT_RECOMENDADOR_REFLEXIVO = """
Eres un experto en literatura.

El usuario se encuentra en un estado de ánimo reflexivo.

Tu objetivo NO es únicamente recomendar libros similares a los que ya ha leído.

Busca libros que despierten la curiosidad, el pensamiento crítico o la reflexión.

Prioriza obras como:

- Misterio
- Thriller psicológico
- Detectives
- Filosofía
- Psicología
- Ciencia
- Historia
- Ensayos
- Divulgación científica
- Novelas con dilemas morales
- Libros que hagan cuestionar ideas o descubrir nuevas perspectivas

Puedes alejarte ligeramente de los géneros favoritos del usuario si eso produce recomendaciones más adecuadas para este estado de ánimo.

Reglas:

- Devuelve únicamente JSON.
- No escribas explicaciones.
- No escribas markdown.
- No escribas texto fuera del JSON.
- Recomienda exactamente cinco libros.
- Todos deben existir realmente.
- No repitas libros.
- No recomiendes libros que el usuario ya posee o haya leído.
- El mensaje debe estar en español.
- Menciona los cinco libros recomendados.
- Termina invitando al usuario a preguntar por cualquiera de ellos.

Formato EXACTO:

{
    "mensaje":"...",
    "libros":[
        {
            "titulo":"...",
            "autor":"..."
        }
    ]
}
"""

PROMPT_RECOMENDADOR_SORPRENDIDO = """
Eres un experto en literatura.

El usuario se encuentra en un estado de ánimo sorprendido.

Tu objetivo es recomendar libros que mantengan
y aumenten esa sensación de sorpresa,
descubrimiento y asombro.

Prioriza obras como:

- Fantasía
- Misterio
- Aventuras
- Ciencia ficción
- Thriller
- Terror
- Mundos imaginarios
- Historias sobrenaturales
- Viajes extraordinarios
- Realidades alternativas
- Historias con giros inesperados
- Libros que permitan descubrir mundos
  completamente diferentes a la realidad cotidiana

Busca libros capaces de despertar curiosidad
y hacer que el lector quiera descubrir
qué ocurrirá después.

Puedes alejarte de los géneros favoritos
del usuario si eso produce recomendaciones
más adecuadas para su estado de ánimo.

Reglas:

- Devuelve únicamente JSON.
- No escribas explicaciones.
- No escribas markdown.
- No escribas texto fuera del JSON.
- Recomienda exactamente cinco libros.
- Todos deben existir realmente.
- No repitas libros.
- No recomiendes libros que el usuario ya posee o haya leído.
- El mensaje debe estar en español.
- Menciona los cinco libros recomendados.
- Termina invitando al usuario a preguntar por cualquiera de ellos.

Formato EXACTO:

{
    "mensaje":"...",
    "libros":[
        {
            "titulo":"...",
            "autor":"..."
        }
    ]
}
"""

PROMPT_RECOMENDADOR_ANSIOSO = """
Eres un experto en literatura.

El usuario se encuentra en un estado de ánimo ansioso.

Tu objetivo es recomendar libros que puedan ayudarle
a desconectarse momentáneamente de sus preocupaciones
y sumergirse en una historia agradable, tranquila
y fácil de disfrutar.

Prioriza especialmente:

- Fantasía reconfortante
- Aventuras ligeras
- Comedia
- Romance
- Ficción reconfortante
- Historias entretenidas y fáciles de seguir
- Mundos imaginativos
- Historias cálidas
- Libros que transmitan sensación de tranquilidad,
  entretenimiento o escapismo

Evita recomendar:

- Terror
- Horror
- Thriller psicológico
- Suspenso intenso
- Historias excesivamente tristes
- Distopías especialmente pesadas
- Historias excesivamente violentas
- Historias perturbadoras
- Libros demasiado densos o complejos

IMPORTANTE:

Aunque alguno de los géneros favoritos del usuario
sea terror, horror, thriller o suspenso, NO debes
utilizar esos géneros como base para las recomendaciones
cuando el usuario se encuentre ansioso.

La prioridad es el estado de ánimo actual del usuario,
no sus géneros favoritos cuando estos puedan resultar
contrarios a una experiencia de lectura tranquila.

La intención no es tratar la ansiedad,
sino ofrecer una experiencia de lectura
agradable, envolvente y sin presión.

Busca libros que permitan al usuario
escapar un rato de sus preocupaciones
y concentrarse en una buena historia.

Reglas:

- Devuelve únicamente JSON.
- No escribas explicaciones.
- No escribas markdown.
- No escribas texto fuera del JSON.
- Recomienda exactamente cinco libros.
- Todos los libros deben existir realmente.
- No repitas libros.
- No recomiendes ningún libro que aparezca en
  la lista "Libros que ya posee o ha leído el usuario".
- Si un libro ya fue leído o pertenece a su biblioteca,
  elige otro.
- El mensaje debe estar en español.
- El mensaje DEBE mencionar explícitamente los cinco
  libros recomendados.
- Debe mencionar cada libro por su título.
- No puede omitir ninguno de los cinco libros.
- El mensaje debe presentar los cinco libros de forma
  natural y agradable, sin utilizar una lista con viñetas.
- El mensaje debe transmitir tranquilidad,
  entretenimiento y la posibilidad de desconectarse
  un rato.
- Termina invitando al usuario a preguntar
  por cualquiera de los cinco libros.
- El mensaje debe ser breve y conciso.
- Debe tener como máximo 80 palabras.

Formato EXACTO:

{
    "mensaje":"...",
    "libros":[
        {
            "titulo":"...",
            "autor":"..."
        }
    ]
}
"""

PROMPT_RECOMENDADOR_TRISTE = """
El usuario se encuentra en un estado de ánimo triste.

A continuación se proporcionará la explicación que
el usuario dio sobre su tristeza.

Debes realizar DOS tareas dentro de una MISMA respuesta:

1. Analizar la explicación del usuario y determinar
   cuál de los cinco estados emocionales corresponde
   mejor a su situación.

2. Utilizando ese estado emocional como guía,
   recomendar exactamente cinco libros.

La clasificación y las recomendaciones deben realizarse
en esta misma llamada.

La prioridad NO es simplemente recomendar libros
del mismo género que el usuario suele leer.

La prioridad principal es respetar la experiencia
emocional indicada.

ESTADO 1 — ABRAZAR LA TRISTEZA

La lectura debe ser predominantemente triste,
profunda, humana y emocional.

Debe acompañar al lector en su tristeza
y permitirle sentirse comprendido.

No es obligatorio que trate sobre el mismo problema
que experimenta el usuario.

La prioridad es la tristeza y la profundidad emocional.

ESTADO 2 — PÉRDIDA O CAMBIO

La lectura debe combinar tristeza con alegría,
belleza, cariño, recuerdos o esperanza.

Debe tratar la pérdida o los cambios de la vida
desde una perspectiva emocionalmente cálida.

La prioridad es:

tristeza + alegría.

ESTADO 3 — INSEGURIDAD O DUDAS SOBRE LA VIDA

La lectura debe provocar reflexión sobre las decisiones,
los caminos posibles, las oportunidades perdidas,
las elecciones y la vida.

La prioridad es que haga reflexionar al lector
sobre su propia vida.

ESTADO 4 — NO ENCUENTRA LO BUENO EN LO MALO

La lectura puede ser triste o dolorosa,
pero debe contener belleza, esperanza,
aceptación o un desenlace reconfortante.

La prioridad es:

tristeza + esperanza.

ESTADO 5 — CASO EXTRAORDINARIO

La respuesta del usuario no encaja claramente
en ninguno de los cuatro estados anteriores.

En ese caso debes crear una orientación personalizada
a partir de la situación emocional del usuario.

No fuerces al usuario dentro de los otros estados.

REGLAS DE CLASIFICACIÓN:

- Selecciona exactamente un estado.
- El estado debe ser un número entre 1 y 5.
- Explica brevemente por qué elegiste ese estado.
- No diagnostiques al usuario.
- No presentes esto como tratamiento psicológico.

REGLAS DE RECOMENDACIÓN:

- Recomienda exactamente cinco libros.
- Todos los libros deben existir realmente.
- No repitas libros.
- No recomiendes ningún libro que el usuario
  ya posea o haya leído.
- Respeta los gustos literarios del usuario cuando
  sea posible.
- La situación emocional tiene prioridad sobre
  la similitud de género.

REGLAS DE RESPUESTA:

- Devuelve únicamente JSON.
- No escribas markdown.
- El mensaje debe estar en español.
- El mensaje debe ser breve.
- El mensaje debe mencionar los cinco libros.
- No hagas el mensaje excesivamente largo.
- Termina invitando al usuario a preguntar
  sobre cualquiera de ellos.

FORMATO EXACTO:

{
    "estado": 1,
    "motivo": "...",
    "mensaje": "...",
    "libros": [
        {
            "titulo": "...",
            "autor": "..."
        }
    ]
}
"""



class RecomendadorLibros:

    def __init__(self):

        self.ia = OrquestadorIA()

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

    def construir_prompt(self, generos, titulos, prompt_base):

        texto = prompt_base

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
            mejor_puntaje = -1

            for resultado in resultados:

                puntaje = 0

                if resultado.get("key"):
                    puntaje += 4

                if resultado.get("portada"):
                    puntaje += 3

                if resultado.get("autor"):
                    puntaje += 2

                if resultado.get("descripcion"):
                    puntaje += 2

                if puntaje > mejor_puntaje:

                    mejor_puntaje = puntaje
                    libro = resultado

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


    def recomendaciones_defecto_reflexivo(self):

        recomendaciones = [

            {
                "titulo": "Crimen y castigo",
                "autor": "Fiódor Dostoievski"
            },

            {
                "titulo": "Sapiens: De animales a dioses",
                "autor": "Yuval Noah Harari"
            },

            {
                "titulo": "El nombre de la rosa",
                "autor": "Umberto Eco"
            },

            {
                "titulo": "Ensayo sobre la ceguera",
                "autor": "José Saramago"
            },

            {
                "titulo": "El mundo de Sofía",
                "autor": "Jostein Gaarder"
            }

        ]

        return self.buscar_libros(recomendaciones)


    def recomendaciones_defecto_sorprendido(self):

        recomendaciones = [

            {
                "titulo": "El Hobbit",
                "autor": "J. R. R. Tolkien"
            },

            {
                "titulo": "Alicia en el país de las maravillas",
                "autor": "Lewis Carroll"
            },

            {
                "titulo": "Viaje al centro de la Tierra",
                "autor": "Julio Verne"
            },

            {
                "titulo": "La historia interminable",
                "autor": "Michael Ende"
            },

            {
                "titulo": "Las crónicas de Narnia",
                "autor": "C. S. Lewis"
            }

        ]

        return self.buscar_libros(recomendaciones)
    
    def recomendaciones_defecto_ansioso(self):

        recomendaciones = [

            {
                "titulo": "La princesa prometida",
                "autor": "William Goldman"
            },

            {
                "titulo": "Harry Potter y la piedra filosofal",
                "autor": "J. K. Rowling"
            },

            {
                "titulo": "El océano al final del camino",
                "autor": "Neil Gaiman"
            },

            {
                "titulo": "Stardust",
                "autor": "Neil Gaiman"
            },

            {
                "titulo": "La brújula dorada",
                "autor": "Philip Pullman"
            }

        ]

        return self.buscar_libros(recomendaciones)

    def recomendar_triste(
        self,
        id_usuario,
        respuesta_usuario
    ):

        print("=" * 60)
        print("RECOMENDADOR TRISTE")
        print("=" * 60)

        generos = self.obtener_generos(
            id_usuario
        )

        titulos = self.obtener_titulos(
            id_usuario
        )

        prompt = PROMPT_RECOMENDADOR_TRISTE

        prompt += "\n\n"
        prompt += "RESPUESTA ORIGINAL DEL USUARIO:\n"
        prompt += respuesta_usuario

        prompt += "\n\n"
        prompt += "LIBROS QUE YA POSEE O HA LEÍDO:\n\n"

        for titulo in titulos:
            prompt += f"- {titulo}\n"

        prompt += "\n"
        prompt += "GÉNEROS FAVORITOS DEL USUARIO:\n\n"

        for genero, cantidad in sorted(
            generos.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            prompt += (
                f"- {genero}: "
                f"{cantidad} libros\n"
            )

        print(prompt)

        try:

            resultado = self.ia.generar_json(
                prompt,
                timeout=45
            )

            estado = resultado.get(
                "estado",
                5
            )

            motivo = resultado.get(
                "motivo",
                ""
            )

            mensaje = resultado.get(
                "mensaje",
                ""
            )

            recomendaciones = resultado.get(
                "libros",
                []
            )

            print("\nESTADO EMOCIONAL:")
            print(estado)

            print("\nMOTIVO:")
            print(motivo)

            print("\nRESPUESTA DEL RECOMENDADOR:")

            for libro in recomendaciones:
                print(
                    f"- {libro['titulo']} | "
                    f"{libro['autor']}"
                )

        except Exception as e:

            print("=" * 60)
            print("ERROR RECOMENDADOR TRISTE")
            print(e)
            print("=" * 60)

            return {
                "estado": 5,
                "motivo": "",
                "mensaje": "",
                "libros": []
            }

        libros = self.buscar_libros(
            recomendaciones
        )

        if len(libros) == 0:

            print(
                "No se encontraron libros "
                "válidos para las recomendaciones."
            )

            return {
                "estado": estado,
                "motivo": motivo,
                "mensaje": mensaje,
                "libros": []
            }

        db.guardar_recomendaciones(
            id_usuario,
            libros
        )

        if mensaje:

            db.guardar_mensaje(
                id_usuario,
                "asistente",
                mensaje
            )

        return {
            "estado": estado,
            "motivo": motivo,
            "mensaje": mensaje,
            "libros": libros
        }



    ##########################################################
    # MÉTODO PRINCIPAL
    ##########################################################

    def recomendar(self, id_usuario, devolver_mensaje=False, tipo=None):

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

            if tipo == "reflexivo":

                libros = self.recomendaciones_defecto_reflexivo()

            elif tipo == "sorprendido":

                libros = self.recomendaciones_defecto_sorprendido()

            elif tipo == "ansioso":

                libros = self.recomendaciones_defecto_ansioso()

            else:

                libros = self.recomendaciones_defecto()

            if devolver_mensaje:

                titulos = [
                    libro["titulo"]
                    for libro in libros
                ]

                if tipo == "reflexivo":

                    mensaje = (
                        "Aunque todavía no tienes libros en tu biblioteca, "
                        "puedes comenzar este momento reflexivo con alguna de estas "
                        "lecturas: "
                        + ", ".join(titulos[:-1])
                        + " o "
                        + titulos[-1]
                        + ". Son historias e ideas que pueden despertar tu curiosidad, "
                        "hacerte cuestionar algunas cosas y abrirte nuevas perspectivas. "
                        "Si alguno te llama especialmente la atención, puedes preguntarme "
                        "por él y podemos hablar sobre lo que puedes encontrar en esa lectura."
                    )

                elif tipo == "sorprendido":

                    mensaje = (
                        "Aunque todavía no tienes libros en tu biblioteca, "
                        "hay muchos mundos por descubrir. Para mantener viva esa "
                        "capacidad de sorprenderte, te propongo "
                        + ", ".join(titulos[:-1])
                        + " y "
                        + titulos[-1]
                        + ". Cada uno puede llevarte a lugares, historias y aventuras "
                        "muy diferentes. Si alguno despierta tu curiosidad, pregúntame "
                        "por él y podemos hablar sobre lo que hace especial a esa lectura."
                    )

                elif tipo == "ansioso":

                    mensaje = (
                        "Si hoy tienes la mente un poco acelerada, "
                        "quizá sea un buen momento para desconectarte "
                        "un rato con una buena historia. Puedes probar con "
                        + ", ".join(titulos[:-1])
                        + " o "
                        + titulos[-1]
                        + ". Son opciones pensadas para dejarte llevar "
                        "por otros mundos, aventuras o historias y olvidarte "
                        "un rato de las preocupaciones. Si alguno te llama "
                        "la atención, puedes preguntarme por él."
                    )

                else:

                    mensaje = (
                        "Como todavía no tienes libros en tu biblioteca, "
                        "te dejo algunas opciones para comenzar tu próxima lectura: "
                        + ", ".join(titulos[:-1])
                        + " o "
                        + titulos[-1]
                        + ". Si alguno te interesa, puedes preguntarme por él."
                    )

                return {
                    "mensaje": mensaje,
                    "libros": libros
                }


        if tipo == "reflexivo":

            prompt_base = PROMPT_RECOMENDADOR_REFLEXIVO

        elif tipo == "sorprendido":

            prompt_base = PROMPT_RECOMENDADOR_SORPRENDIDO

        elif tipo == "ansioso":

            prompt_base = PROMPT_RECOMENDADOR_ANSIOSO

        else:

            prompt_base = PROMPT_RECOMENDADOR



        prompt = self.construir_prompt(
            generos,
            titulos,
            prompt_base
        )


        print("\nENVIANDO PROMPT A GEMINI...")
        print("-" * 60)
        print(prompt)
        print("-" * 60)

        try:

            recomendaciones = self.ia.generar_json(prompt)

            mensaje = recomendaciones.get(
                "mensaje",
                ""
            )

            recomendaciones = recomendaciones.get(
                "libros",
                []
            )

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

        if mensaje:

            db.guardar_mensaje(
                id_usuario,
                "asistente",
                mensaje
            )


        if len(libros) == 0:
            libros = self.recomendaciones_defecto()

            if devolver_mensaje:
                return {
                    "mensaje": mensaje,
                    "libros": libros
                }

            return libros

        if devolver_mensaje:
            return {
                "mensaje": mensaje,
                "libros": libros
            }

        return libros


recomendador_bp = Blueprint(
    "recomendador",
    __name__
)

motor = RecomendadorLibros()

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

