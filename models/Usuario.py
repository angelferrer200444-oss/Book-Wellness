import mysql.connector

from db import obtener_conexion


class Usuario:

    def __init__(
        self,
        id_usuario=None,
        nombre=None,
        correo=None,
        password=None
    ):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.password = password


    def registrar(self):
        """
        Registra el usuario en la base de datos y
        devuelve el ID asignado.
        """

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO usuarios
            (nombre, correo, password)
            VALUES (%s, %s, %s)
        """, (
            self.nombre,
            self.correo,
            self.password
        ))

        conexion.commit()

        self.id_usuario = cursor.lastrowid

        # Guarda temporalmente el usuario para la encuesta.
        cursor.execute("""
            DELETE FROM usuario_encuesta_temporal
        """)

        cursor.execute("""
            INSERT INTO usuario_encuesta_temporal
            (id_usuario)
            VALUES (%s)
        """, (self.id_usuario,))

        conexion.commit()

        cursor.close()
        conexion.close()

        return self.id_usuario


    @classmethod
    def iniciar_sesion(cls, correo, password):
        """
        Busca un usuario en la base de datos.
        Si existe, devuelve un objeto Usuario.
        """

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_usuario, nombre, correo
            FROM usuarios
            WHERE correo = %s
            AND password = %s
        """, (
            correo,
            password
        ))

        datos = cursor.fetchone()

        cursor.close()
        conexion.close()

        if not datos:
            return None

        return cls(
            id_usuario=datos["id_usuario"],
            nombre=datos["nombre"],
            correo=datos["correo"]
        )


    # @classmethod
    # def recuperar_password(cls, correo):
    #     """
    #     Busca un usuario mediante su correo y
    #     comienza el proceso de recuperación de contraseña.
    #     (Pendiente de implementar)
    #     """
    #     


    def cerrar_sesion(self):
        """
        Actualmente Flask maneja la sesión.
        Se deja este método reservado para futuras
        implementaciones.
        """
        pass
