from db import obtener_conexion

class Preferencias:

    def __init__(
        self,
        id_usuario=None,
        nivel=None,
        respuestas=None
    ):
        self.id_usuario = id_usuario
        self.nivel = nivel
        self.respuestas = respuestas


    @classmethod
    def obtener_usuario_pendiente(cls):
        """
        Obtiene el ID del usuario que debe
        completar la encuesta.
        """

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id_usuario
            FROM usuario_encuesta_temporal
            LIMIT 1
        """)

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if not fila:
            return None

        return fila[0]


    @classmethod
    def obtener_preguntas(cls, nivel):
        """
        Obtiene las preguntas correspondientes
        al nivel seleccionado.
        """

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_pregunta, nombre_campo
            FROM preguntas_encuesta
            WHERE nivel = %s
            ORDER BY id_pregunta
        """, (nivel,))

        preguntas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return preguntas


    def guardar(self):
        """
        Guarda las respuestas de la encuesta.
        """

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        preguntas = self.obtener_preguntas(
            self.nivel
        )

        for pregunta in preguntas:

            respuesta = self.respuestas.get(
                pregunta["nombre_campo"]
            )

            if isinstance(respuesta, list):
                respuesta = ", ".join(respuesta)

            cursor.execute("""
                INSERT INTO respuestas_encuesta
                (id_usuario, id_pregunta, respuesta)
                VALUES (%s, %s, %s)
            """, (
                self.id_usuario,
                pregunta["id_pregunta"],
                respuesta
            ))

        conexion.commit()

        cursor.close()
        conexion.close()


    @classmethod
    def limpiar_usuario_pendiente(cls, id_usuario):
        """
        Elimina al usuario de la tabla temporal
        una vez finalizada la encuesta.
        """

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            DELETE FROM usuario_encuesta_temporal
            WHERE id_usuario = %s
        """, (id_usuario,))

        conexion.commit()

        cursor.close()
        conexion.close()
