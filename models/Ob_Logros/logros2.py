from db import obtener_conexion


class Logros2:

    # ==========================================
    # CONFIGURACIÓN
    # ==========================================

    GENEROS_AVENTURA = [
        "adventure",
        "aventura",
        "action",
        "acción",
        "fantasy",
        "fantasía"
    ]

    GENEROS_MISTERIO = [
        "mystery",
        "misterio",
        "thriller",
        "suspense",
        "crime",
        "crimen",
        "policial"
    ]

    # ==========================================
    # MÉTODO PRINCIPAL
    # ==========================================

    @staticmethod
    def obtener_logros(usuario_id):
        return [
            Logros2.primeros_pasos(usuario_id),
            Logros2.devorador_de_paginas(usuario_id),
            Logros2.explorador_de_mundos(usuario_id),
            Logros2.detective_literario(usuario_id),
            Logros2.mente_constante(usuario_id),
            Logros2.anotador_estrella(usuario_id),
            Logros2.bibliofilo(usuario_id)
        ]

    # ==========================================
    # 8. PRIMEROS PASOS
    # ==========================================

    @staticmethod
    def primeros_pasos(usuario_id):

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
        objetivo = 1

        progreso = min(
            libros_leidos,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 8,
            "nombre": "Primeros Pasos",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_leidos >= objetivo
        }

    # ==========================================
    # 9. DEVORADOR DE PÁGINAS
    # ==========================================

    @staticmethod
    def devorador_de_paginas(usuario_id):

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
        objetivo = 100

        progreso = min(
            paginas_leidas,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 9,
            "nombre": "Devorador de Páginas",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": paginas_leidas >= objetivo
        }

    # ==========================================
    # 10. EXPLORADOR DE MUNDOS
    # ==========================================

    @staticmethod
    def explorador_de_mundos(usuario_id):

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

        paginas_aventura = 0

        for lectura in lecturas:

            genero = lectura.get("genero")

            if not genero:
                continue

            genero = str(genero).lower()

            pertenece = any(
                palabra in genero
                for palabra in Logros2.GENEROS_AVENTURA
            )

            if pertenece:
                paginas_aventura += lectura["paginas_leidas"]

        objetivo = 100

        progreso = min(
            paginas_aventura,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 10,
            "nombre": "Explorador de Mundos",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": paginas_aventura >= objetivo
        }

    # ==========================================
    # 11. DETECTIVE LITERARIO
    # ==========================================

    @staticmethod
    def detective_literario(usuario_id):

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
                INSTR(LOWER(genero), 'misterio') > 0
                OR INSTR(LOWER(genero), 'mystery') > 0
                OR INSTR(LOWER(genero), 'thriller') > 0
                OR INSTR(LOWER(genero), 'crimen') > 0
                OR INSTR(LOWER(genero), 'crime') > 0
            )
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        libros_misterio = resultado["libros"] or 0
        objetivo = 1

        progreso = min(
            libros_misterio,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 11,
            "nombre": "Detective Literario",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_misterio >= objetivo
        }

    # ==========================================
    # 12. MENTE CONSTANTE
    # ==========================================

    @staticmethod
    def mente_constante(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(DISTINCT DATE(fecha_lectura)) AS dias
            FROM lecturas
            WHERE id_usuario = %s
            AND paginas_leidas > 0
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        dias_registrados = resultado["dias"] or 0
        objetivo = 3

        progreso = min(
            dias_registrados,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 12,
            "nombre": "Mente Constante",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": dias_registrados >= objetivo
        }

    # ==========================================
    # 13. ANOTADOR ESTRELLA
    # ==========================================

    @staticmethod
    def anotador_estrella(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(id_nota) AS notas
            FROM notas_usuario
            WHERE id_usuario = %s
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        total_notas = resultado["notas"] or 0
        objetivo = 5

        progreso = min(
            total_notas,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 13,
            "nombre": "Anotador Estrella",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": total_notas >= objetivo
        }

    # ==========================================
    # 14. BIBLIÓFILO
    # ==========================================

    @staticmethod
    def bibliofilo(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(DISTINCT id_libro) AS libros
            FROM libros
            WHERE id_usuario = %s
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        total_libros = resultado["libros"] or 0
        objetivo = 5

        progreso = min(
            total_libros,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 14,
            "nombre": "Bibliófilo",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": total_libros >= objetivo
        }