# calendario.py
# Clase encargada de armar la vista de calendario: qué días tienen
# actividad de lectura (sesión iniciada) o fecha límite de un libro,
# y qué libros corresponden a un día específico.

from db import obtener_conexion

class Calendario:

    @staticmethod
    def obtener_fechas_calendario(id_usuario):
        """
        Devuelve un diccionario {fecha: tipo} con todos los días que tienen
        alguna actividad relevante para el usuario:
        - 'sesion': el usuario inició una lectura ese día (fecha_inicio)
        - 'fin_libro': ese día es la fecha límite de un libro
        Si un mismo día tiene ambos tipos, se prioriza 'fin_libro' para
        que el calendario resalte los vencimientos por encima de las sesiones normales.
        """
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT DATE(fecha_inicio) as fecha, 'primera_sesion' as tipo
            FROM lecturas
            WHERE id_usuario = %s AND fecha_inicio IS NOT NULL

            UNION

            SELECT DATE(fecha_limite) as fecha,
                CASE WHEN fecha_limite < CURDATE() THEN 'expirada' ELSE 'fecha_limite' END as tipo
            FROM lecturas
            WHERE id_usuario = %s AND fecha_limite IS NOT NULL
            AND estado != 'He terminado el libro'

            UNION

            SELECT DATE(fecha_fin) as fecha, 'concluido' as tipo
            FROM lecturas
            WHERE id_usuario = %s AND fecha_fin IS NOT NULL
            AND estado = 'He terminado el libro'

            UNION

            SELECT DATE(fecha) as fecha, 'sesion' as tipo
            FROM sesiones
            WHERE id_usuario = %s AND fecha IS NOT NULL
        """, (id_usuario, id_usuario, id_usuario, id_usuario))

        filas = cursor.fetchall()
        cursor.close()
        conexion.close()

        # Se recorren las filas para quedarnos con un solo tipo por fecha,
        # priorizando 'fin_libro' si hay conflicto
        fechas = {}
        for fila in filas:
            fecha_str = str(fila['fecha'])
            if fecha_str not in fechas:
                fechas[fecha_str] = fila['tipo']
            else:
                # prioridad: concluido > fecha_limite > sesion
                prioridad = {'concluido': 4, 'fecha_limite': 3, 'primera_sesion': 2, 'sesion': 1}
                if prioridad.get(fila['tipo'], 0) > prioridad.get(fechas[fecha_str], 0):
                    fechas[fecha_str] = fila['tipo']

        return fechas

    @staticmethod
    def obtener_libros_por_fecha(id_usuario, fecha):
        """
        Devuelve los libros asociados a una fecha específica del calendario,
        ya sea porque el usuario empezó una sesión de lectura ese día
        o porque ese día es la fecha límite de terminar el libro.
        Se usa cuando el usuario hace clic en un día del calendario.
        """
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.titulo, l.autor, l.portada, l.id_libro,
                   'sesion' as tipo
            FROM lecturas lec
            JOIN libros l ON lec.id_libro = l.id_libro
            WHERE lec.id_usuario = %s AND DATE(lec.fecha_inicio) = %s
            UNION
            SELECT l.titulo, l.autor, l.portada, l.id_libro,
                   'fecha_limite' as tipo
            FROM lecturas lec
            JOIN libros l ON lec.id_libro = l.id_libro
            WHERE lec.id_usuario = %s AND DATE(lec.fecha_limite) = %s
        """, (id_usuario, fecha, id_usuario, fecha))
        libros = cursor.fetchall()
        cursor.close()
        conexion.close()
        return libros
    @staticmethod
    def guardar_fecha_limite(id_usuario, id_libro, fecha_limite):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE lecturas SET fecha_limite = %s
            WHERE id_usuario = %s AND id_libro = %s
        """, (fecha_limite, id_usuario, id_libro))
        conexion.commit()
        cursor.close()
        conexion.close()