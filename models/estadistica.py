from db import obtener_conexion
from datetime import date, timedelta
from collections import Counter


class Estadistica:

    @staticmethod
    def consultar(id_usuario):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Páginas y tiempo total
        cursor.execute("""
            SELECT
                COALESCE(SUM(paginas_leidas), 0) AS total_paginas,
                COALESCE(SUM(tiempo_minutos), 0) AS total_minutos,
                COALESCE(AVG(tiempo_minutos), 0) AS tiempo_promedio
            FROM lecturas
            WHERE id_usuario = %s
        """, (id_usuario,))

        totales = cursor.fetchone()

        # Palabras nuevas registradas
        cursor.execute("""
            SELECT contenido
            FROM notas_usuario
            WHERE id_usuario = %s
            AND categoria = 'Vocabulario'
        """, (id_usuario,))

        filas_palabras = cursor.fetchall()

        palabras_nuevas = 0

        for fila in filas_palabras:
            contenido = fila["contenido"]

            if contenido:
                palabras_nuevas += len([
                    palabra
                    for palabra in contenido.split(",")
                    if palabra.strip()
                ])
                
        # Libros leídos
        cursor.execute("""
            SELECT COUNT(*) AS libros_leidos
            FROM libros
            WHERE id_usuario = %s
            AND categoria = 'Leído'
        """, (id_usuario,))

        leidos = cursor.fetchone()


        # Estado de ánimo más frecuente
        cursor.execute("""
            SELECT
                nl.como_te_sientes,
                COUNT(*) AS freq
            FROM notas_lectura nl
            JOIN lecturas l
                ON nl.id_lectura = l.id_lectura
            WHERE l.id_usuario = %s
            AND nl.como_te_sientes IS NOT NULL
            GROUP BY nl.como_te_sientes
            ORDER BY freq DESC
            LIMIT 1
        """, (id_usuario,))

        animo = cursor.fetchone()

        # Géneros preferidos
        cursor.execute("""
            SELECT genero
            FROM libros
            WHERE id_usuario = %s
            AND genero IS NOT NULL
            AND genero != ''
        """, (id_usuario,))

        filas_generos = cursor.fetchall()

        contador = Counter()

        for fila in filas_generos:

            for g in fila["genero"].split(","):

                g = g.strip()

                if g:
                    contador[g] += 1

        generos_top = [
            g
            for g, _ in contador.most_common(3)
        ]

        # Días con sesión registrada
        cursor.execute("""
            SELECT DISTINCT DATE(fecha_fin) AS dia
            FROM lecturas
            WHERE id_usuario = %s
            AND fecha_fin IS NOT NULL
            ORDER BY dia ASC
        """, (id_usuario,))

        dias = [
            fila["dia"]
            for fila in cursor.fetchall()
        ]

        cursor.close()
        conexion.close()

        racha_actual, racha_maxima = (
            Estadistica._calcular_rachas(dias)
        )

        return {

            "total_paginas":
                totales["total_paginas"],

            "total_minutos":
                totales["total_minutos"],

            "tiempo_promedio":
                Estadistica._formatear_tiempo(
                    totales["tiempo_promedio"]
                ),
            
            "tiempo_total_formateado":
                Estadistica._formatear_tiempo(
                    totales["total_minutos"]
                ),



            "palabras_nuevas":
                palabras_nuevas,

            "libros_leidos":
                leidos["libros_leidos"],

            "animo":
                animo["como_te_sientes"]
                if animo
                else "Sin datos",

            "generos_top":
                generos_top,

            "racha_actual":
                racha_actual,

            "racha_maxima":
                racha_maxima
        }

    @staticmethod
    def _calcular_rachas(dias):

        racha_actual = 0
        racha_maxima = 0
        racha_temp = 1

        if not dias:
            return racha_actual, racha_maxima

        for i in range(1, len(dias)):

            if (
                dias[i] - dias[i - 1]
            ).days == 1:

                racha_temp += 1

                racha_maxima = max(
                    racha_maxima,
                    racha_temp
                )

            else:

                racha_temp = 1

        racha_maxima = max(
            racha_maxima,
            racha_temp
        )

        hoy = date.today()

        if (
            dias[-1] == hoy
            or dias[-1] == hoy - timedelta(days=1)
        ):
            racha_actual = 1

            for i in range(
                len(dias) - 1,
                0,
                -1
            ):

                if (
                    dias[i] - dias[i - 1]
                ).days == 1:

                    racha_actual += 1

                else:

                    break

        return racha_actual, racha_maxima

    @staticmethod
    def _formatear_tiempo(minutos):
        minutos = float(minutos or 0)

        if minutos < 1:
            segundos = round(minutos * 60, 1)
            return f"{segundos:.0f} s"

        if minutos < 60:
            return f"{minutos:.1f} Min"

        horas = minutos / 60
        return f"{horas:.1f} h"
