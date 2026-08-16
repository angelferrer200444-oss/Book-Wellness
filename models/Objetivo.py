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




