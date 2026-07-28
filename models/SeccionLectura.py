from db import obtener_conexion


class SeccionLectura:

    def __init__(
        self,
        id_lectura=None,
        id_usuario=None,
        id_libro=None,
        tiempo_minutos=0,
        estado="en progreso",
        fecha_inicio=None,
        fecha_fin=None,
        paginas_leidas=0,
        pagina_actual=0,
        capitulos_leidos=0
    ):

        self.id_lectura = id_lectura
        self.id_usuario = id_usuario
        self.id_libro = id_libro
        self.tiempo_minutos = tiempo_minutos
        self.estado = estado
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.paginas_leidas = paginas_leidas
        self.pagina_actual = pagina_actual
        self.capitulos_leidos = capitulos_leidos

    @classmethod
    def obtener(cls, id_usuario, id_libro):
        """
        Obtiene la sesión de lectura correspondiente
        al usuario y al libro.
        """

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM lecturas
            WHERE id_usuario = %s
            AND id_libro = %s
        """, (
            id_usuario,
            id_libro
        ))

        lectura = cursor.fetchone()

        cursor.close()
        conexion.close()

        return lectura

    def actualizar_progreso(self):
            """
            Actualiza el progreso de la sesión de lectura.
            Si la lectura no existe, la crea.
            """

            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT id_lectura
                FROM lecturas
                WHERE id_usuario = %s
                AND id_libro = %s
            """, (
                self.id_usuario,
                self.id_libro
            ))

            existente = cursor.fetchone()

            if existente:

                campos = "pagina_actual = %s, capitulos_leidos = %s"
                valores = [
                    self.pagina_actual,
                    self.capitulos_leidos
                ]

                if self.fecha_inicio:
                    campos += ", fecha_inicio = %s"
                    valores.append(self.fecha_inicio)

                valores.extend([
                    self.id_usuario,
                    self.id_libro
                ])

                cursor.execute(f"""
                    UPDATE lecturas
                    SET {campos}
                    WHERE id_usuario = %s
                    AND id_libro = %s
                """, valores)

            else:

                cursor.execute("""
                    INSERT INTO lecturas
                    (
                        id_usuario,
                        id_libro,
                        pagina_actual,
                        capitulos_leidos,
                        fecha_inicio
                    )
                    VALUES
                    (%s, %s, %s, %s, %s)
                """, (
                    self.id_usuario,
                    self.id_libro,
                    self.pagina_actual,
                    self.capitulos_leidos,
                    self.fecha_inicio
                ))

                self.id_lectura = cursor.lastrowid

            conexion.commit()
            cursor.close()
            conexion.close()

    def guardar(self):
            """
            Guarda una sesión de lectura. Si ya existe una
            para el usuario y el libro, actualiza sus datos
            acumulando el tiempo, páginas y capítulos leídos.
            """

            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    id_lectura,
                    tiempo_minutos,
                    paginas_leidas,
                    capitulos_leidos
                FROM lecturas
                WHERE id_usuario = %s
                AND id_libro = %s
            """, (
                self.id_usuario,
                self.id_libro
            ))

            existente = cursor.fetchone()

            if existente:

                nuevo_tiempo = (
                    existente["tiempo_minutos"] +
                    self.tiempo_minutos
                )

                nuevas_paginas = (
                    existente["paginas_leidas"] +
                    self.paginas_leidas
                )

                nuevos_capitulos = (
                    existente["capitulos_leidos"] +
                    self.capitulos_leidos
                )

                cursor.execute("""
                    UPDATE lecturas
                    SET
                        tiempo_minutos = %s,
                        paginas_leidas = %s,
                        pagina_actual = %s,
                        capitulos_leidos = %s,
                        estado = %s,
                        fecha_fin = %s
                    WHERE id_lectura = %s
                """, (
                    nuevo_tiempo,
                    nuevas_paginas,
                    self.pagina_actual,
                    nuevos_capitulos,
                    self.estado,
                    self.fecha_fin,
                    existente["id_lectura"]
                ))

                self.id_lectura = existente["id_lectura"]

            else:

                cursor.execute("""
                    INSERT INTO lecturas
                    (
                        id_usuario,
                        id_libro,
                        tiempo_minutos,
                        estado,
                        fecha_inicio,
                        fecha_fin,
                        paginas_leidas,
                        pagina_actual,
                        capitulos_leidos
                    )
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    self.id_usuario,
                    self.id_libro,
                    self.tiempo_minutos,
                    self.estado,
                    self.fecha_fin,
                    self.fecha_fin,
                    self.paginas_leidas,
                    self.pagina_actual,
                    self.capitulos_leidos
                ))

                self.id_lectura = cursor.lastrowid

            conexion.commit()
            cursor.close()
            conexion.close()

            return self.id_lectura

        