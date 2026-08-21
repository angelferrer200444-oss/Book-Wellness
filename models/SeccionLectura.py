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
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM lecturas
            WHERE id_usuario = %s AND id_libro = %s
        """, (id_usuario, id_libro))
        lectura = cursor.fetchone()
        cursor.close()
        conexion.close()
        return lectura

    def actualizar_progreso(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_lectura FROM lecturas
            WHERE id_usuario = %s AND id_libro = %s
        """, (self.id_usuario, self.id_libro))
        existente = cursor.fetchone()

        if existente:
            campos = "pagina_actual = %s, capitulos_leidos = %s"
            valores = [self.pagina_actual, self.capitulos_leidos]
            if self.fecha_inicio:
                campos += ", fecha_inicio = %s"
                valores.append(self.fecha_inicio)
            valores.extend([self.id_usuario, self.id_libro])
            cursor.execute(f"""
                UPDATE lecturas SET {campos}
                WHERE id_usuario = %s AND id_libro = %s
            """, valores)
        else:
            cursor.execute("""
                INSERT INTO lecturas
                (id_usuario, id_libro, pagina_actual, capitulos_leidos, fecha_inicio)
                VALUES (%s, %s, %s, %s, %s)
            """, (self.id_usuario, self.id_libro, self.pagina_actual, self.capitulos_leidos, self.fecha_inicio))
            self.id_lectura = cursor.lastrowid

        conexion.commit()
        cursor.close()
        conexion.close()

    def guardar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_lectura, tiempo_minutos, paginas_leidas, capitulos_leidos
            FROM lecturas
            WHERE id_usuario = %s AND id_libro = %s
        """, (self.id_usuario, self.id_libro))
        existente = cursor.fetchone()

        if existente:
            nuevo_tiempo = (existente["tiempo_minutos"] or 0) + (self.tiempo_minutos or 0)
            nuevas_paginas = (existente["paginas_leidas"] or 0) + (self.paginas_leidas or 0)
            nuevos_capitulos = (existente["capitulos_leidos"] or 0) + (self.capitulos_leidos or 0)

            cursor.execute("""
                UPDATE lecturas
                SET tiempo_minutos = %s, paginas_leidas = %s, pagina_actual = %s,
                    capitulos_leidos = %s, estado = %s, fecha_fin = %s
                WHERE id_lectura = %s
            """, (nuevo_tiempo, nuevas_paginas, self.pagina_actual, nuevos_capitulos,
                  self.estado, self.fecha_fin, existente["id_lectura"]))
            self.id_lectura = existente["id_lectura"]
        else:
            cursor.execute("""
                INSERT INTO lecturas
                (id_usuario, id_libro, tiempo_minutos, estado, fecha_inicio, fecha_fin,
                 paginas_leidas, pagina_actual, capitulos_leidos)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (self.id_usuario, self.id_libro, self.tiempo_minutos, self.estado,
                  self.fecha_fin, self.fecha_fin, self.paginas_leidas, self.pagina_actual,
                  self.capitulos_leidos))
            self.id_lectura = cursor.lastrowid

        conexion.commit()
        cursor.close()
        conexion.close()
        return self.id_lectura

    def guardar_sesion(self, como_te_sientes=None):
        print("GUARDANDO SESION:", self.id_lectura, self.id_usuario, self.fecha_fin)
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO sesiones
            (id_lectura, id_usuario, fecha, paginas_leidas_sesion, tiempo_minutos, capitulos_leidos, como_te_sientes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            self.id_lectura,
            self.id_usuario,
            self.fecha_fin,
            self.paginas_leidas,
            self.tiempo_minutos,
            self.capitulos_leidos,
            como_te_sientes
        ))
        conexion.commit()
        cursor.close()
        conexion.close()
        