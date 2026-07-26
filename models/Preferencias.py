import db


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
    def obtener_preguntas(cls, nivel):
        """
        Obtiene las preguntas correspondientes
        al nivel seleccionado.
        """

        print(f"[Preferencias] Obteniendo preguntas del nivel: {nivel}")

        return db.obtener_preguntas_por_nivel(
            nivel
        )


    def guardar(self):
        """
        Guarda las respuestas de la encuesta
        del usuario.
        """

        print(f"[Preferencias] Guardando respuestas del usuario {self.id_usuario}")

        # Llama al método para comprobar que pasa por la clase.
        # De momento no usamos el resultado porque db.py
        # ya vuelve a consultar las preguntas.
        self.obtener_preguntas(
            self.nivel
        )

        db.guardar_respuestas_encuesta(
            self.id_usuario,
            self.nivel,
            self.respuestas
        )

        print("[Preferencias] Respuestas guardadas correctamente.")

