import random
import db
from db import ( obtener_conexion, guardar_mensaje )
from models.Libro import Libro
from .respuestafeliz import ( RESPUESTAS_FELIZ, RESPUESTAS_FELIZ_SIN_LIBRO )
from IA.orquestador import OrquestadorIA
from IA.recomendador import motor

class EstadoAnimo:

    ##########################################################
    # METODOS DB
    ##########################################################

    @staticmethod
    def guardar(id_usuario, estado):

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO estado_animo_actual
            (id_usuario, estado_animo)
            VALUES (%s, %s)
        """, (id_usuario, estado))

        conexion.commit()

        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_actual(id_usuario):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT estado_animo, fecha_hora
            FROM estado_animo_actual
            WHERE id_usuario = %s
            ORDER BY fecha_hora DESC
            LIMIT 1
        """, (id_usuario,))

        estado = cursor.fetchone()

        cursor.close()
        conexion.close()

        return estado

    @staticmethod
    def obtener_libro_leyendo(id_usuario):

        libros = Libro.obtener_libros_usuario(
            id_usuario,
            "leyendo"
        )

        if libros:
            return random.choice(libros)

        return None

    @staticmethod
    def obtener_libro_pendiente(id_usuario):

        libros = Libro.obtener_libros_usuario(
            id_usuario,
            "pendiente"
        )

        if libros:
            return random.choice(libros)

        return None

    @staticmethod
    def obtener_libro_reflexivo(id_usuario):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                titulo,
                genero
            FROM libros
            WHERE id_usuario = %s
        """, (id_usuario,))

        libros = cursor.fetchall()

        cursor.close()
        conexion.close()

        palabras = [

            "misterio",
            "thriller",
            "suspenso",
            "filosofia",
            "filosofía",
            "psicologia",
            "psicología",
            "ciencia",
            "historia",
            "ensayo",
            "detective",
            "crimen"

        ]

        for libro in libros:

            texto = (
                (libro["titulo"] or "")
                + " "
                + (libro["genero"] or "")
            ).lower()

            if any(
                palabra in texto
                for palabra in palabras
            ):

                return libro

        return None

    @staticmethod
    def obtener_libro_sorprendido(id_usuario):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                titulo,
                genero
            FROM libros
            WHERE id_usuario = %s
        """, (id_usuario,))

        libros = cursor.fetchall()

        cursor.close()
        conexion.close()

        palabras = [

            "fantasia",
            "fantasía",
            "fantasy",

            "misterio",
            "mystery",

            "thriller",
            "suspenso",

            "aventura",
            "aventuras",
            "adventure",

            "ciencia ficcion",
            "ciencia ficción",
            "science fiction",
            "sci-fi",

            "terror",
            "horror",

            "magia",
            "magic",

            "sobrenatural",
            "supernatural",

            "distopia",
            "distopía",
            "dystopia",

            "ficcion",
            "ficción",

            "fantastico",
            "fantástico"

        ]

        for libro in libros:

            texto = (
                (libro["titulo"] or "")
                + " "
                + (libro["genero"] or "")
            ).lower()

            if any(
                palabra in texto
                for palabra in palabras
            ):

                return libro

        return None

    @staticmethod
    def obtener_libro_ansioso(id_usuario):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                titulo,
                genero
            FROM libros
            WHERE id_usuario = %s
        """, (id_usuario,))

        libros = cursor.fetchall()

        cursor.close()
        conexion.close()

        palabras = [

            "romance",
            "romántico",
            "romantico",

            "comedia",
            "comedy",

            "fantasia",
            "fantasía",
            "fantasy",

            "aventura",
            "aventuras",
            "adventure",

            "juvenile",
            "young adult",
            "juvenil",

            "children",
            "infantil",

            "slice of life",

            "amistad",
            "friendship",

            "familia",
            "family",

            "feel good",
            "cozy",

            "humor",
            "humour"

        ]

        palabras_excluidas = [

            "terror",
            "horror",

            "thriller",

            "suspenso",
            "suspense",

            "misterio",
            "mystery",

            "crimen",
            "crime",

            "gore",

            "violencia",
            "violence",

            "dark",
            "dark fiction",

            "distopia",
            "distopía",
            "dystopia",

            "psicológico",
            "psicologico",
            "psychological"

        ]

        for libro in libros:

            texto = (
                (libro["titulo"] or "")
                + " "
                + (libro["genero"] or "")
            ).lower()

            if any(
                palabra in texto
                for palabra in palabras_excluidas
            ):
                continue

            if any(
                palabra in texto
                for palabra in palabras
            ):

                return libro

        return None



    ##########################################################
    # METODOS EMOCIONES
    ##########################################################

    @staticmethod
    def responder_feliz(id_usuario):

        libro = EstadoAnimo.obtener_libro_leyendo(id_usuario)

        if libro:

            mensaje = random.choice(RESPUESTAS_FELIZ)

            mensaje = mensaje.format(
                libro=libro["titulo"]
            )

        else:

            mensaje = random.choice(
                RESPUESTAS_FELIZ_SIN_LIBRO
            )

        guardar_mensaje(
            id_usuario,
            "ia",
            mensaje
        )

        return mensaje

    @staticmethod
    def responder_tranquilo(id_usuario):

        libro_leyendo = EstadoAnimo.obtener_libro_leyendo(
            id_usuario
        )

        libro_pendiente = EstadoAnimo.obtener_libro_pendiente(
            id_usuario
        )


        libro = libro_leyendo

        if libro is None:
            libro = libro_pendiente

        if libro:

            contexto = f"""
            Libro recomendado:

            Título: {libro["titulo"]}
            """

        else:

            contexto = """
            El usuario no tiene libros
            leyendo ni pendientes.
            """
        
        prompt = f"""
        El usuario indicó que hoy se siente tranquilo.

        Tu objetivo es ayudar a mantener ese estado.

        No recomiendes libros nuevos.

        Si existe un libro de su biblioteca,
        recomiéndale continuar con él.

        Invítalo a leer sin prisas.

        Sugiere desconectarse un rato
        de las obligaciones.

        Habla de forma cálida,
        natural y cercana.

        No uses listas.

        Máximo 90 palabras.

        {contexto}
        """

        ia = OrquestadorIA()

        respuesta = ia.generar_respuesta(
            id_usuario,
            prompt
        )

        return respuesta

    @staticmethod
    def responder_reflexivo(id_usuario):

        print("===== REFLEXIVO =====")

        libro = EstadoAnimo.obtener_libro_reflexivo(
            id_usuario
        )

        print("Libro encontrado:", libro)

        # ======================================================
        # CASO 1: EL USUARIO YA TIENE UN LIBRO REFLEXIVO
        # ======================================================

        if libro:

            print("Usando libro de la biblioteca.")

            prompt = f"""
            El usuario indicó que hoy se siente reflexivo.

            Tiene este libro en su biblioteca:

            Título: {libro["titulo"]}

            Recomiéndale continuar con ese libro.

            Habla de forma cercana,
            natural y cálida.

            Relaciona la lectura con su estado
            de ánimo reflexivo.

            Invítalo a descubrir nuevas ideas,
            reflexionar o cuestionarse cosas.

            No uses listas.

            Máximo 100 palabras.
            """

            print("Enviando prompt a Gemini...")

            ia = OrquestadorIA()

            respuesta = ia.generar_respuesta(
                id_usuario,
                prompt
            )

            print("Gemini respondió.")

            return {
                "respuesta": respuesta,
                "recomendaciones": []
            }


        # ======================================================
        # CASO 2: NO TIENE UN LIBRO REFLEXIVO
        # ======================================================

        print(
            "No encontré libro. "
            "Llamando al recomendador..."
        )

        resultado = motor.recomendar(
            id_usuario,
            devolver_mensaje=True,
            tipo="reflexivo"
        )

        recomendaciones = resultado["libros"]

        respuesta = resultado["mensaje"]


        # ======================================================
        # GUARDAR NUEVAS RECOMENDACIONES
        # ======================================================

        db.guardar_recomendaciones(
            id_usuario,
            recomendaciones
        )

        print("CACHE ACTUALIZADO")

        print(
            f"Recomendaciones guardadas: "
            f"{len(recomendaciones)}"
        )


        # ======================================================
        # GUARDAR MENSAJE GENERADO POR EL RECOMENDADOR
        # ======================================================

        db.guardar_mensaje(
            id_usuario,
            "ia",
            respuesta
        )


        print("Devolviendo respuesta CON recomendaciones.")

        return {
            "respuesta": respuesta,
            "recomendaciones": recomendaciones
        }

    @staticmethod
    def responder_sorprendido(id_usuario):

        print("===== SORPRENDIDO =====")

        libro = EstadoAnimo.obtener_libro_sorprendido(
            id_usuario
        )

        print("Libro encontrado:", libro)


        # ======================================================
        # CASO 1: EL USUARIO YA TIENE UN LIBRO ADECUADO
        # ======================================================

        if libro:

            print("Usando libro de la biblioteca.")

            prompt = f"""
            El usuario indicó que hoy se siente sorprendido.

            Tiene este libro en su biblioteca:

            Título: {libro["titulo"]}

            Recomiéndale continuar con ese libro.

            Relaciona la lectura con su estado
            de ánimo sorprendido.

            Hazle sentir curiosidad por lo que
            puede descubrir dentro de la historia.

            Habla de forma cercana,
            natural y cálida.

            Invítalo a dejarse sorprender
            por la lectura.

            No uses listas.

            Máximo 100 palabras.
            """

            print("Enviando prompt a Gemini...")

            ia = OrquestadorIA()

            respuesta = ia.generar_respuesta(
                id_usuario,
                prompt
            )

            print("Gemini respondió.")

            return {
                "respuesta": respuesta,
                "recomendaciones": []
            }


        # ======================================================
        # CASO 2: NO TIENE UN LIBRO ADECUADO
        # ======================================================

        print(
            "No encontré libro. "
            "Llamando al recomendador..."
        )

        resultado = motor.recomendar(
            id_usuario,
            devolver_mensaje=True,
            tipo="sorprendido"
        )

        recomendaciones = resultado["libros"]

        respuesta = resultado["mensaje"]


        # ======================================================
        # GUARDAR NUEVAS RECOMENDACIONES
        # ======================================================

        db.guardar_recomendaciones(
            id_usuario,
            recomendaciones
        )

        print("CACHE ACTUALIZADO")

        print(
            f"Recomendaciones guardadas: "
            f"{len(recomendaciones)}"
        )


        # ======================================================
        # GUARDAR MENSAJE
        # ======================================================

        db.guardar_mensaje(
            id_usuario,
            "ia",
            respuesta
        )


        print(
            "Devolviendo respuesta CON recomendaciones."
        )

        return {
            "respuesta": respuesta,
            "recomendaciones": recomendaciones
        }

    @staticmethod
    def responder_ansioso(id_usuario):

        print("===== ANSIOSO =====")

        libro = EstadoAnimo.obtener_libro_ansioso(
            id_usuario
        )

        print("Libro encontrado:", libro)

        # ======================================================
        # CASO 1: EL USUARIO YA TIENE UN LIBRO ADECUADO
        # ======================================================

        if libro:

            print("Usando libro de la biblioteca.")

            prompt = f"""
            El usuario indicó que hoy se siente ansioso.

            Tiene este libro en su biblioteca:

            Título: {libro["titulo"]}

            Recomiéndale continuar con ese libro.

            La intención es ayudarlo a desconectarse
            un poco de sus preocupaciones y disfrutar
            de la lectura sin presión.

            Habla de forma cercana,
            natural y cálida.

            No presentes la lectura como un tratamiento
            para la ansiedad.

            Invítalo simplemente a tomarse un momento,
            avanzar a su propio ritmo y dejarse llevar
            por la historia.

            No uses listas.

            Máximo 100 palabras.
            """

            print("Enviando prompt a Gemini...")

            ia = OrquestadorIA()

            respuesta = ia.generar_respuesta(
                id_usuario,
                prompt
            )

            print("Gemini respondió.")

            return {
                "respuesta": respuesta,
                "recomendaciones": []
            }

        # ======================================================
        # CASO 2: NO TIENE UN LIBRO ADECUADO
        # ======================================================

        print(
            "No encontré libro. "
            "Llamando al recomendador..."
        )

        resultado = motor.recomendar(
            id_usuario,
            devolver_mensaje=True,
            tipo="ansioso"
        )

        recomendaciones = resultado["libros"]

        respuesta = resultado["mensaje"]

        # ======================================================
        # GUARDAR RECOMENDACIONES
        # ======================================================

        db.guardar_recomendaciones(
            id_usuario,
            recomendaciones
        )

        print("CACHE ACTUALIZADO")

        print(
            f"Recomendaciones guardadas: "
            f"{len(recomendaciones)}"
        )

        return {
            "respuesta": respuesta,
            "recomendaciones": recomendaciones
        }


        