import db

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
        # -------------------------
        # Registra el usuario en la base de datos y devuelve
        # el ID asignado.
        # -------------------------

        self.id_usuario = db.registrar_usuario(
            self.nombre,
            self.correo,
            self.password
        )

        return self.id_usuario


    @classmethod
    def iniciar_sesion(cls, correo, password):
        #     -------------------------
        #       Busca un usuario en la base de datos.
        #       Si existe, devuelve un objeto Usuario.
        #     -------------------------

        datos = db.buscar_usuario(
            correo,
            password
        )

        if not datos:
            return None

        return cls(
            id_usuario=datos["id_usuario"],
            nombre=datos["nombre"],
            correo=correo
        )


    # @classmethod
    # def recuperar_password(cls, correo):
    #     -------------------------
    #     Busca un usuario mediante su correo y
    #     comienza el proceso de recuperación de contraseña.
    #     (Pendiente de implementar)
    #     -------------------------
    #     pass


    def cerrar_sesion(self):
        # -------------------------
        # Actualmente Flask maneja la sesión.
        # -------------------------
        pass
