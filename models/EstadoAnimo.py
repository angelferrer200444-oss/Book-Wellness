from db import obtener_conexion


class EstadoAnimo:

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
