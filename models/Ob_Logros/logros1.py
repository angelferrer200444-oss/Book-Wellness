from db import obtener_conexion


class Logros1:

    # ==========================================
    # MÉTODO PRINCIPAL
    # ==========================================

    @staticmethod
    def obtener_logros(usuario_id):
        return [
            Logros1.devorador_de_paginas(usuario_id),
            Logros1.habito_nocturno(usuario_id),
            Logros1.lector_critico(usuario_id),
            Logros1.primeros_pasos(usuario_id),
            Logros1.enfoque_de_hierro(usuario_id),
            Logros1.maraton_dominical(usuario_id),
            Logros1.racha_imbatible(usuario_id)
        ]

    # ==========================================
    # HELPER: RACHA MÁXIMA DE DÍAS CONSECUTIVOS
    # ==========================================

    @staticmethod
    def _racha_maxima(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT DISTINCT DATE(fecha) AS dia
            FROM sesiones
            WHERE id_usuario = %s
            ORDER BY dia ASC
        """, (usuario_id,))

        filas = cursor.fetchall()

        cursor.close()
        conexion.close()

        if not filas:
            return 0

        dias = [fila["dia"] for fila in filas]

        racha_actual = 1
        racha_maxima = 1

        for i in range(1, len(dias)):

            diferencia = (dias[i] - dias[i - 1]).days

            if diferencia == 1:
                racha_actual += 1
            elif diferencia > 1:
                racha_actual = 1

            racha_maxima = max(racha_maxima, racha_actual)

        return racha_maxima

    # ==========================================
    # 1. DEVORADOR DE PÁGINAS
    # ==========================================

    @staticmethod
    def devorador_de_paginas(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT COALESCE(SUM(paginas_leidas), 0) AS paginas
            FROM lecturas
            WHERE id_usuario = %s
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        paginas_leidas = resultado["paginas"] or 0
        objetivo = 500

        progreso = min(paginas_leidas, objetivo)
        porcentaje = min(int((progreso / objetivo) * 100), 100)

        return {
            "id": 1,
            "nombre": "Devorador de Páginas",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": paginas_leidas >= objetivo
        }

    # ==========================================
    # 2. HÁBITO NOCTURNO
    # ==========================================

    @staticmethod
    def habito_nocturno(usuario_id):

        racha = Logros1._racha_maxima(usuario_id)
        objetivo = 15

        progreso = min(racha, objetivo)
        porcentaje = min(int((progreso / objetivo) * 100), 100)

        return {
            "id": 2,
            "nombre": "Hábito Nocturno",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": racha >= objetivo
        }

    # ==========================================
    # 3. LECTOR CRÍTICO
    # ==========================================

    @staticmethod
    def lector_critico(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM notas_usuario
            WHERE id_usuario = %s
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        notas_escritas = resultado["total"] or 0
        objetivo = 10

        progreso = min(notas_escritas, objetivo)
        porcentaje = min(int((progreso / objetivo) * 100), 100)

        return {
            "id": 3,
            "nombre": "Lector Crítico",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": notas_escritas >= objetivo
        }

    # ==========================================
    # 4. PRIMEROS PASOS
    # ==========================================

    @staticmethod
    def primeros_pasos(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT COUNT(DISTINCT id_libro) AS libros
            FROM libros
            WHERE id_usuario = %s
            AND categoria = 'leido'
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        libros_leidos = resultado["libros"] or 0
        objetivo = 1

        progreso = min(libros_leidos, objetivo)
        porcentaje = min(int((progreso / objetivo) * 100), 100)

        return {
            "id": 4,
            "nombre": "Primeros Pasos",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": libros_leidos >= objetivo
        }

    # ==========================================
    # 5. ENFOQUE DE HIERRO
    # ==========================================

    @staticmethod
    def enfoque_de_hierro(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT COALESCE(MAX(tiempo_minutos), 0) AS max_tiempo
            FROM sesiones
            WHERE id_usuario = %s
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        mejor_sesion = resultado["max_tiempo"] or 0
        objetivo = 120

        progreso = min(mejor_sesion, objetivo)
        porcentaje = min(int((progreso / objetivo) * 100), 100)

        return {
            "id": 5,
            "nombre": "Enfoque de Hierro",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": mejor_sesion >= objetivo
        }

    # ==========================================
    # 6. MARATÓN DOMINICAL
    # ==========================================

    @staticmethod
    def maraton_dominical(usuario_id):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT COALESCE(MAX(paginas_dia), 0) AS mejor_dia
            FROM (
                SELECT DATE(fecha) AS dia,
                       SUM(paginas_leidas_sesion) AS paginas_dia
                FROM sesiones
                WHERE id_usuario = %s
                GROUP BY DATE(fecha)
            ) AS dias_agrupados
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        mejor_dia = resultado["mejor_dia"] or 0
        objetivo = 100

        progreso = min(mejor_dia, objetivo)
        porcentaje = min(int((progreso / objetivo) * 100), 100)

        return {
            "id": 6,
            "nombre": "Maratón Dominical",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": mejor_dia >= objetivo
        }

    # ==========================================
    # 7. RACHA IMBATIBLE
    # ==========================================

    @staticmethod
    def racha_imbatible(usuario_id):

        racha = Logros1._racha_maxima(usuario_id)
        objetivo = 30

        progreso = min(racha, objetivo)
        porcentaje = min(int((progreso / objetivo) * 100), 100)

        return {
            "id": 7,
            "nombre": "Racha Imbatible",
            "progreso": progreso,
            "objetivo": objetivo,
            "porcentaje": porcentaje,
            "completado": racha >= objetivo
        }