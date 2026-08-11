from db import obtener_conexion


class Logros3:

    # ==========================================
    # CONFIGURACIÓN
    # ==========================================

    GENEROS_MENTE_SANA = [
        "salud",
        "health",
        "bienestar",
        "wellness",
        "habitos",
        "hábitos",
        "self-help",
        "self help",
        "autoayuda",
        "psicologia",
        "psicología",
        "psychology"
    ]

    # ==========================================
    # MÉTODO PRINCIPAL
    # ==========================================

    @staticmethod
    def obtener_logros(usuario_id):
        return [
            Logros3.mente_sana(usuario_id),
            Logros3.gran_volumen(usuario_id),
            Logros3.lector_versatil(usuario_id),
            Logros3.vision_del_futuro(usuario_id),
            Logros3.mitad_de_camino(usuario_id),
            Logros3.cronicas_reales(usuario_id),
            Logros3.lexic_enriquecido(usuario_id)
        ]


    # ==========================================
    # 15. MENTE SANA
    # ==========================================

    @staticmethod
    def mente_sana(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                l.paginas_leidas,
                b.genero
            FROM lecturas l
            INNER JOIN libros b
                ON l.id_libro = b.id_libro
            WHERE l.id_usuario = %s
            AND b.id_usuario = %s
            AND l.paginas_leidas > 0
        """, (
            usuario_id,
            usuario_id
        ))

        lecturas = cursor.fetchall()

        cursor.close()
        conexion.close()

        paginas_salud = 0

        for lectura in lecturas:

            genero = lectura.get("genero")

            if not genero:
                continue

            genero = str(genero).lower()

            pertenece = any(
                palabra in genero
                for palabra in Logros3.GENEROS_MENTE_SANA
            )

            if pertenece:
                paginas_salud += lectura["paginas_leidas"]

        objetivo = 150

        progreso = min(
            paginas_salud,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 15,
            "nombre": "Mente Sana",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": paginas_salud >= objetivo
        }

    # ==========================================
    # 16. GRAN VOLUMEN
    # ==========================================

    @staticmethod
    def gran_volumen(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COALESCE(SUM(paginas_leidas), 0) AS paginas
            FROM lecturas
            WHERE id_usuario = %s
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        paginas_leidas = resultado["paginas"] or 0

        objetivo = 400

        progreso = min(
            paginas_leidas,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 16,
            "nombre": "Gran Volumen",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": paginas_leidas >= objetivo
        }

    # ==========================================
    # 17. LECTOR VERSÁTIL
    # ==========================================

    @staticmethod
    def lector_versatil(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(DISTINCT id_libro) AS libros
            FROM lecturas
            WHERE id_usuario = %s
            AND fecha_inicio IS NOT NULL
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        libros_iniciados = resultado["libros"] or 0
        objetivo = 2

        progreso = min(
            libros_iniciados,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 17,
            "nombre": "Lector Versátil",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_iniciados >= objetivo
        }

    # ==========================================
    # 18. VISIÓN DEL FUTURO
    # ==========================================

    @staticmethod
    def vision_del_futuro(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(DISTINCT id_libro) AS libros
            FROM libros
            WHERE id_usuario = %s
            AND categoria = 'leido'
            AND genero IS NOT NULL
            AND (
                INSTR(LOWER(genero), 'ciencia ficción') > 0
                OR INSTR(LOWER(genero), 'ciencia ficcion') > 0
                OR INSTR(LOWER(genero), 'science fiction') > 0
            )
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        libros_scifi = resultado["libros"] or 0

        objetivo = 2

        progreso = min(
            libros_scifi,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 18,
            "nombre": "Visión del Futuro",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_scifi >= objetivo
        }


    # ==========================================
    # 19. MITAD DE CAMINO
    # ==========================================

    @staticmethod
    def mitad_de_camino(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(DISTINCT id_libro) AS libros
            FROM libros
            WHERE id_usuario = %s
            AND categoria = 'leido'
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        libros_leidos = resultado["libros"] or 0

        objetivo = 12

        progreso = min(
            libros_leidos,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 19,
            "nombre": "Mitad de Camino",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_leidos >= objetivo
        }


    # ==========================================
    # 20. CRÓNICAS REALES
    # ==========================================

    @staticmethod
    def cronicas_reales(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(DISTINCT id_libro) AS libros
            FROM libros
            WHERE id_usuario = %s
            AND categoria = 'leido'
            AND genero IS NOT NULL
            AND (
                INSTR(LOWER(genero), 'historia') > 0
                OR INSTR(LOWER(genero), 'history') > 0
                OR INSTR(LOWER(genero), 'biografía') > 0
                OR INSTR(LOWER(genero), 'biografia') > 0
                OR INSTR(LOWER(genero), 'biography') > 0
                OR INSTR(LOWER(genero), 'biographies') > 0
                OR INSTR(LOWER(genero), 'biography & autobiography') > 0
            )
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        libros_historia = resultado["libros"] or 0

        objetivo = 1

        progreso = min(
            libros_historia,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 20,
            "nombre": "Crónicas Reales",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_historia >= objetivo
        }

    # ==========================================
    # 21. LÉXICO ENRIQUECIDO
    # ==========================================

    @staticmethod
    def lexic_enriquecido(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT contenido
            FROM notas_usuario
            WHERE id_usuario = %s
            AND categoria = 'Vocabulario'
            AND contenido IS NOT NULL
        """, (usuario_id,))

        notas = cursor.fetchall()

        cursor.close()
        conexion.close()

        palabras = 0

        for nota in notas:

            contenido = str(
                nota["contenido"]
            ).strip()

            if contenido:
                palabras += len(
                    contenido.split()
                )

        objetivo = 20

        progreso = min(
            palabras,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 21,
            "nombre": "Léxico Enriquecido",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": palabras >= objetivo
        }
