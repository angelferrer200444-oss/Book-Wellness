# seguimiento.py
# Clase que arma la lista de eventos de un día específico para la
# sección de Seguimiento: sesiones de lectura registradas ese día y
# libros cuya fecha límite cae ese día.

from db import obtener_conexion

class Seguimiento:

    @staticmethod
    def obtener_eventos_por_fecha(id_usuario, fecha):
        """
        Devuelve una lista combinada de eventos para una fecha dada:
        - sesiones de lectura que el usuario inició ese día, con su progreso
          (páginas leídas, tiempo, capítulos leídos)
        - libros cuya fecha límite es ese día, con su estado actual
        Cada evento incluye un campo 'tipo' ('sesion' o 'fecha_limite')
        para que el frontend sepa cómo mostrarlo.
        """
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Sesiones de lectura iniciadas en la fecha dada
        cursor.execute("""
            SELECT l.titulo, l.autor, l.portada, l.id_libro,
                   lec.paginas_leidas, lec.tiempo_minutos,
                   lec.fecha_inicio, lec.capitulos_leidos,
                   'sesion' as tipo
            FROM lecturas lec
            JOIN libros l ON lec.id_libro = l.id_libro
            WHERE lec.id_usuario = %s AND DATE(lec.fecha_inicio) = %s
        """, (id_usuario, fecha))
        sesiones = cursor.fetchall()

        # Libros cuya fecha límite cae en la fecha dada
        cursor.execute("""
            SELECT l.titulo, l.autor, l.portada, l.id_libro,
                   lec.fecha_limite, lec.estado,
                   'fecha_limite' as tipo
            FROM lecturas lec
            JOIN libros l ON lec.id_libro = l.id_libro
            WHERE lec.id_usuario = %s AND DATE(lec.fecha_limite) = %s
        """, (id_usuario, fecha))
        limites = cursor.fetchall()

        cursor.close()
        conexion.close()

        # Se combinan ambos tipos en una sola lista para el día consultado
        return sesiones + limites