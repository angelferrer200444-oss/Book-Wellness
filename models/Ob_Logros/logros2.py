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

    GENEROS_FANTASIA = [
        "fantasy",
        "fantasía"
    ]

    # ==========================================
    # MÉTODO PRINCIPAL
    # ==========================================

    @staticmethod
    def obtener_logros(usuario_id):
        return [
            Logros2.explorador_de_misterio(usuario_id),
            Logros2.viaje_fantastico(usuario_id),
            Logros2.paso_a_paso(usuario_id),
            
            Logros2.erudito(usuario_id),
            Logros2.lector_veloz(usuario_id),
            Logros2.amor_por_los_clasicos(usuario_id)
        ]

    # ==========================================
    # 8. EXPLORADOR DE MISTERIO
    # ==========================================

    @staticmethod
    def explorador_de_misterio(usuario_id):

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
                OR INSTR(LOWER(genero), 'suspense') > 0
                OR INSTR(LOWER(genero), 'crimen') > 0
                OR INSTR(LOWER(genero), 'crime') > 0
                OR INSTR(LOWER(genero), 'policial') > 0
            )
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        libros_misterio = resultado["libros"] or 0
        objetivo = 2

        progreso = min(
            libros_misterio,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 8,
            "nombre": "Explorador de Misterio",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_misterio >= objetivo
        }

    # ==========================================
    # 9. VIAJE FANTÁSTICO
    # ==========================================

    @staticmethod
    def viaje_fantastico(usuario_id):

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
                INSTR(LOWER(genero), 'fantasy') > 0
                OR INSTR(LOWER(genero), 'fantasía') > 0
            )
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        libros_fantasia = resultado["libros"] or 0
        objetivo = 3

        progreso = min(
            libros_fantasia,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 9,
            "nombre": "Viaje Fantástico",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_fantasia >= objetivo
        }

    # ==========================================
    # 10. PASO A PASO
    # ==========================================

    @staticmethod
    def paso_a_paso(usuario_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COALESCE(SUM(capitulos_leidos), 0) AS capitulos
            FROM lecturas
            WHERE id_usuario = %s
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        capitulos_leidos = resultado["capitulos"] or 0
        objetivo = 25

        progreso = min(
            capitulos_leidos,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 10,
            "nombre": "Paso a Paso",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": capitulos_leidos >= objetivo
        }

    # ==========================================
    # 11. Explorador del alba: Pendiente hasta colocar un sistema de horas
    # ==========================================

    # ==========================================
    # 12. ERUDITO
    # ==========================================

    @staticmethod
    def erudito(usuario_id):

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
        objetivo = 5

        progreso = min(
            libros_leidos,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 12,
            "nombre": "Erudito",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_leidos >= objetivo
        }

    # ==========================================
    # 13. LECTOR VELOZ
    # ==========================================

    @staticmethod
    def lector_veloz(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(DISTINCT id_libro) AS libros
            FROM lecturas
            WHERE id_usuario = %s
            AND estado = 'terminado'
            AND fecha_inicio IS NOT NULL
            AND fecha_fin IS NOT NULL
            AND DATEDIFF(fecha_fin, fecha_inicio) <= 2
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        libros_veloces = resultado["libros"] or 0
        objetivo = 1

        progreso = min(
            libros_veloces,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )
        return {
            "id": 13,
            "nombre": "Lector Veloz",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_veloces >= objetivo
        }

    # ==========================================
    # 14. AMOR POR LOS CLÁSICOS
    # ==========================================

    @staticmethod
    def amor_por_los_clasicos(usuario_id):

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
                INSTR(LOWER(genero), 'classic') > 0
                OR INSTR(LOWER(genero), 'clásico') > 0
                OR INSTR(LOWER(genero), 'clasico') > 0
                OR INSTR(LOWER(genero), 'literatura clásica') > 0
                OR INSTR(LOWER(genero), 'literatura clasica') > 0
            )
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        libros_clasicos = resultado["libros"] or 0
        objetivo = 1

        progreso = min(
            libros_clasicos,
            objetivo
        )

        porcentaje = min(
            int((progreso / objetivo) * 100),
            100
        )

        return {
            "id": 14,
            "nombre": "Amor por los Clásicos",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_clasicos >= objetivo
        }
