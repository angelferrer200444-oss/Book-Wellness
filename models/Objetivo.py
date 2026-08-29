from db import obtener_conexion


class Objetivo:

    def __init__(
        self,
        id_usuario,
        titulo,
        descripcion,
        tipo,
        meta,
        unidad=None,
        fecha_inicio=None,
        fecha_fin=None,
        condicion_tipo=None,
        condicion_valor=None,
        frecuencia=None,
        id_objetivo=None,
        progreso_actual=0,
        completado=False,
        estado="activo"
    ):

        self.id_objetivo = id_objetivo
        self.id_usuario = id_usuario
        self.titulo = titulo
        self.descripcion = descripcion
        self.tipo = tipo
        self.meta = meta
        self.unidad = unidad
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.condicion_tipo = condicion_tipo
        self.condicion_valor = condicion_valor
        self.frecuencia = frecuencia
        self.progreso_actual = progreso_actual
        self.completado = completado
        self.estado = estado


    def actualizar_progreso(self, cantidad):

        self.progreso_actual += cantidad

        if self.progreso_actual >= self.meta:
            self.progreso_actual = self.meta
            self.estado = "completado"
            self.completado = True

    def calcular_progreso(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        try:
            # -------------------------------------------------
            # RUTINA
            # -------------------------------------------------

            if self.tipo == "rutina":

                sql = """
                    SELECT COUNT(DISTINCT s.fecha) AS total_dias
                    FROM sesiones s
                    WHERE s.id_usuario = %s
                    AND s.fecha >= %s
                """

                valores = [
                    self.id_usuario,
                    self.fecha_inicio
                ]

                if self.fecha_fin:
                    sql += " AND s.fecha <= %s"
                    valores.append(self.fecha_fin)

                cursor.execute(sql, valores)

                resultado = cursor.fetchone()

                progreso = resultado["total_dias"] or 0

            # -------------------------------------------------
            # LIBROS
            # -------------------------------------------------

            elif self.tipo == "libros":

                sql = """
                    SELECT COUNT(DISTINCT l.id_libro) AS total
                    FROM sesiones s
                    INNER JOIN lecturas l
                        ON s.id_lectura = l.id_lectura
                    INNER JOIN libros b
                        ON l.id_libro = b.id_libro
                    WHERE s.id_usuario = %s
                    AND s.fecha >= %s
                    AND l.estado = 'He terminado el libro'
                """

                valores = [
                    self.id_usuario,
                    self.fecha_inicio
                ]

                if self.fecha_fin:
                    sql += " AND s.fecha <= %s"
                    valores.append(self.fecha_fin)

                sql, valores = self._aplicar_condicion(
                    sql,
                    valores
                )

                cursor.execute(sql, valores)

                resultado = cursor.fetchone()

                progreso = resultado["total"] or 0


            # -------------------------------------------------
            # PÁGINAS
            # -------------------------------------------------

            elif self.tipo == "paginas":

                sql = """
                    SELECT COALESCE(
                        SUM(s.paginas_leidas_sesion),
                        0
                    ) AS total
                    FROM sesiones s
                    INNER JOIN lecturas l
                        ON s.id_lectura = l.id_lectura
                    INNER JOIN libros b
                        ON l.id_libro = b.id_libro
                    WHERE s.id_usuario = %s
                    AND s.fecha >= %s
                """

                valores = [
                    self.id_usuario,
                    self.fecha_inicio
                ]

                if self.fecha_fin:
                    sql += " AND s.fecha <= %s"
                    valores.append(self.fecha_fin)

                sql, valores = self._aplicar_condicion(
                    sql,
                    valores
                )

                cursor.execute(sql, valores)

                resultado = cursor.fetchone()

                progreso = resultado["total"] or 0

            # -------------------------------------------------
            # TIEMPO
            # -------------------------------------------------

            elif self.tipo == "tiempo":

                sql = """
                    SELECT COALESCE(
                        SUM(s.tiempo_minutos),
                        0
                    ) AS total
                    FROM sesiones s
                    INNER JOIN lecturas l
                        ON s.id_lectura = l.id_lectura
                    INNER JOIN libros b
                        ON l.id_libro = b.id_libro
                    WHERE s.id_usuario = %s
                    AND s.fecha >= %s
                """

                valores = [
                    self.id_usuario,
                    self.fecha_inicio
                ]

                if self.fecha_fin:
                    sql += " AND s.fecha <= %s"
                    valores.append(self.fecha_fin)

                sql, valores = self._aplicar_condicion(
                    sql,
                    valores
                )

                cursor.execute(sql, valores)

                resultado = cursor.fetchone()

                progreso = resultado["total"] or 0
            
            else:

                progreso = 0

            # -------------------------------------------------
            # LIMITAR A LA META
            # -------------------------------------------------

            progreso = min(
                progreso,
                self.meta
            )

            self.progreso_actual = progreso

            # -------------------------------------------------
            # COMPLETADO
            # -------------------------------------------------

            if self.progreso_actual >= self.meta:

                self.progreso_actual = self.meta
                self.completado = True
                self.estado = "completado"

            else:

                self.completado = False
                self.estado = "activo"

            return self.progreso_actual

        finally:

            cursor.close()
            conexion.close()

    def _aplicar_condicion(self, sql, valores):

        condicion = self.condicion_tipo
        valor = self.condicion_valor

        # ---------------------------------------------
        # SIN CONDICIÓN
        # ---------------------------------------------

        if not condicion or condicion == "ninguna":
            return sql, valores

        # ---------------------------------------------
        # GÉNERO
        # ---------------------------------------------

        if condicion == "genero":

            sql += """
                AND b.genero LIKE %s
            """

            valores.append(
                f"%{valor}%"
            )

        # ---------------------------------------------
        # AUTOR
        # ---------------------------------------------

        elif condicion == "autor":

            sql += """
                AND b.autor LIKE %s
            """

            valores.append(
                f"%{valor}%"
            )

        # ---------------------------------------------
        # FORMATO
        # ---------------------------------------------

        elif condicion == "formato":

            sql += """
                AND b.formato LIKE %s
            """

            valores.append(
                f"%{valor}%"
            )

        # ---------------------------------------------
        # LIBRO
        # ---------------------------------------------

        elif condicion == "libro":

            sql += """
                AND b.titulo LIKE %s
            """

            valores.append(
                f"%{valor}%"
            )

        return sql, valores

    def recalcular_y_guardar(self):

        self.calcular_progreso()

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            UPDATE objetivos_personales
            SET
                progreso_actual = %s,
                completado = %s,
                estado = %s,
                porcentaje = %s
            WHERE id_objetivo = %s
        """

        porcentaje = self.obtener_porcentaje()

        valores = (
            self.progreso_actual,
            self.completado,
            self.estado,
            porcentaje,
            self.id_objetivo
        )

        cursor.execute(
            sql,
            valores
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return self


    def obtener_porcentaje(self):

        if self.meta <= 0:
            return 0

        porcentaje = (self.progreso_actual / self.meta) * 100

        return min(100, porcentaje)


    def esta_completado(self):

        return self.progreso_actual >= self.meta


    def to_dict(self):

        return {
            "id_objetivo": self.id_objetivo,
            "id_usuario": self.id_usuario,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "tipo": self.tipo,
            "meta": self.meta,
            "unidad": self.unidad,
            "progreso_actual": self.progreso_actual,
            "porcentaje": self.obtener_porcentaje(),

            "fecha_inicio": str(self.fecha_inicio) if self.fecha_inicio else None,

            "fecha_fin": str(self.fecha_fin) if self.fecha_fin else None,

            "condicion_tipo": self.condicion_tipo,
            "condicion_valor": self.condicion_valor,
            "frecuencia": self.frecuencia,
            "estado": self.estado
        }


    @staticmethod
    def crear(objetivo):

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO objetivos_personales
        (
            id_usuario,
            titulo,
            descripcion,
            tipo,
            meta,
            unidad,
            fecha_inicio,
            fecha_fin,
            condicion_tipo,
            condicion_valor,
            frecuencia
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        valores = (
            objetivo.id_usuario,
            objetivo.titulo,
            objetivo.descripcion,
            objetivo.tipo,
            objetivo.meta,
            objetivo.unidad,
            objetivo.fecha_inicio,
            objetivo.fecha_fin,
            objetivo.condicion_tipo,
            objetivo.condicion_valor,
            objetivo.frecuencia
        )

        print("VALORES INSERT:", valores)

        cursor.execute(sql, valores)

        conexion.commit()

        objetivo.id_objetivo = cursor.lastrowid

        cursor.close()
        conexion.close()

        return objetivo

    @staticmethod
    def obtener_por_usuario(id_usuario):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM objetivos_personales
            WHERE id_usuario=%s
            """,
            (id_usuario,)
        )

        datos = cursor.fetchall()

        cursor.close()
        conexion.close()

        objetivos = []

        for dato in datos:

            objetivo = Objetivo(
                id_objetivo=dato["id_objetivo"],
                id_usuario=dato["id_usuario"],
                titulo=dato["titulo"],
                descripcion=dato["descripcion"],
                tipo=dato["tipo"],
                meta=dato["meta"],
                unidad=dato["unidad"],
                fecha_inicio=dato["fecha_inicio"],
                fecha_fin=dato["fecha_fin"],
                condicion_tipo=dato["condicion_tipo"],
                condicion_valor=dato["condicion_valor"],
                frecuencia=dato["frecuencia"],
                progreso_actual=dato["progreso_actual"],
                completado=dato["completado"],
                estado=dato["estado"]
            )

            print("TIPO DEL OBJETO:", objetivo.tipo)

            objetivo.calcular_progreso()

            objetivos.append(
                objetivo.to_dict()
            )


        return objetivos

    @staticmethod
    def obtener_por_id(id_objetivo):

        conexion = obtener_conexion()

        cursor = conexion.cursor(dictionary=True)


        cursor.execute(
            """
            SELECT *
            FROM objetivos_personales
            WHERE id_objetivo = %s
            """,
            (id_objetivo,)
        )


        datos = cursor.fetchone()


        cursor.close()
        conexion.close()


        if datos is None:
            return None


        return Objetivo(
            id_objetivo=datos["id_objetivo"],
            id_usuario=datos["id_usuario"],
            titulo=datos["titulo"],
            descripcion=datos["descripcion"],
            tipo=datos["tipo"],
            meta=datos["meta"],
            unidad=datos["unidad"],
            fecha_inicio=datos["fecha_inicio"],
            fecha_fin=datos["fecha_fin"],
            condicion_tipo=datos["condicion_tipo"],
            condicion_valor=datos["condicion_valor"],
            frecuencia=datos["frecuencia"],
            progreso_actual=datos["progreso_actual"],
            completado=datos["completado"],
            estado=datos["estado"]
        )

    @staticmethod
    def actualizar(objetivo):

        conexion = obtener_conexion()

        cursor = conexion.cursor()


        sql = """
        UPDATE objetivos_personales
        SET
            titulo = %s,
            descripcion = %s,
            tipo = %s,
            meta = %s,
            unidad = %s,
            fecha_inicio = %s,
            fecha_fin = %s,
            condicion_tipo = %s,
            condicion_valor = %s,
            frecuencia = %s,
            progreso_actual = %s,
            completado = %s,
            estado = %s
        WHERE id_objetivo = %s
        """


        valores = (

            objetivo.titulo,

            objetivo.descripcion,

            objetivo.tipo,

            objetivo.meta,

            objetivo.unidad,

            objetivo.fecha_inicio,

            objetivo.fecha_fin,

            objetivo.condicion_tipo,

            objetivo.condicion_valor,

            objetivo.frecuencia,

            objetivo.progreso_actual,

            objetivo.completado,

            objetivo.estado,

            objetivo.id_objetivo

        )


        cursor.execute(sql, valores)

        conexion.commit()


        cursor.close()

        conexion.close()


        return objetivo

    @staticmethod
    def eliminar(id_objetivo):

        conexion = obtener_conexion()

        cursor = conexion.cursor()


        cursor.execute(
            """
            DELETE FROM objetivos_personales
            WHERE id_objetivo = %s
            """,
            (id_objetivo,)
        )


        eliminado = cursor.rowcount > 0


        conexion.commit()


        cursor.close()

        conexion.close()


        return eliminado
