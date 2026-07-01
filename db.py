# database.py
import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='proyectowellness',
        port=3306
    )

def registrar_usuario(nombre, correo, password):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, correo, password) VALUES (%s, %s, %s)",
        (nombre, correo, password)
    )
    conexion.commit()
    id_generado = cursor.lastrowid
    cursor.close()
    conexion.close()
    return id_generado

def buscar_usuario(correo, password):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_usuario, nombre, correo FROM usuarios WHERE correo = %s AND password = %s",
        (correo, password)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    return usuario

def agregar_libro(id_usuario, titulo, autor, descripcion, portada, categoria, key_libro, paginas, id_google=None, genero=None, anio=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    print("ID_GOOGLE RECIBIDO:", id_google)
    
    cursor.execute("""
        SELECT id_libro FROM libros 
        WHERE id_usuario = %s AND titulo = %s
    """, (id_usuario, titulo))
    
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        return False

    cursor.execute("""
        INSERT INTO libros (id_usuario, titulo, autor, descripcion, portada, categoria, key_libro, paginas_totales, id_google, genero, anio) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (id_usuario, titulo, autor, descripcion, portada, categoria, key_libro, paginas, id_google, genero, anio))
    conexion.commit()
    cursor.close()
    conexion.close()
    return True

def obtener_libros_usuario(id_usuario, categoria):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_libro, titulo, autor, portada, key_libro, id_google FROM libros 
        WHERE id_usuario = %s AND categoria = %s
    """, (id_usuario, categoria))
    libros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return libros

def eliminar_libro(id_libro, id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        DELETE FROM libros 
        WHERE id_libro = %s AND id_usuario = %s
    """, (id_libro, id_usuario))
    conexion.commit()
    cursor.close()
    conexion.close()
    

def obtener_libro(id_libro):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM libros WHERE id_libro = %s
    """, (id_libro,))
    libro = cursor.fetchone()
    cursor.close()
    conexion.close()
    return libro

def actualizar_datos_libro(id_libro, paginas_totales=None, num_caps=None, formato=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    campos = []
    valores = []
    
    if paginas_totales is not None:
        campos.append("paginas_totales = %s")
        valores.append(paginas_totales)
    
    if num_caps is not None:
        campos.append("num_caps = %s")
        valores.append(num_caps)
    
    if formato is not None:
        campos.append("formato = %s")
        valores.append(formato)
    
    if campos:
        valores.append(id_libro)
        query = f"UPDATE libros SET {', '.join(campos)} WHERE id_libro = %s"
        cursor.execute(query, valores)
        conexion.commit()
    
    cursor.close()
    conexion.close()


def guardar_lectura(id_usuario, id_libro, tiempo_minutos, estado, fecha_fin, paginas_leidas, pagina_actual, capitulos_leidos):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_lectura, tiempo_minutos, paginas_leidas, capitulos_leidos 
        FROM lecturas 
        WHERE id_usuario = %s AND id_libro = %s
    """, (id_usuario, id_libro))
    
    existente = cursor.fetchone()

    if existente:
        nuevo_tiempo = existente['tiempo_minutos'] + tiempo_minutos
        nuevas_paginas = existente['paginas_leidas'] + paginas_leidas
        nuevos_capitulos = existente['capitulos_leidos'] + capitulos_leidos

        cursor.execute("""
            UPDATE lecturas 
            SET tiempo_minutos = %s, paginas_leidas = %s, pagina_actual = %s, capitulos_leidos = %s,
                estado = %s, fecha_fin = %s
            WHERE id_lectura = %s
        """, (nuevo_tiempo, nuevas_paginas, pagina_actual, nuevos_capitulos, estado, fecha_fin, existente['id_lectura']))
        
        id_lectura = existente['id_lectura']

    else:
        cursor.execute("""
            INSERT INTO lecturas (id_usuario, id_libro, tiempo_minutos, estado, fecha_inicio, fecha_fin, paginas_leidas, pagina_actual, capitulos_leidos)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id_usuario, id_libro, tiempo_minutos, estado, fecha_fin, fecha_fin, paginas_leidas, pagina_actual, capitulos_leidos))
        
        id_lectura = cursor.lastrowid

    conexion.commit()
    cursor.close()
    conexion.close()
    return id_lectura

def guardar_fecha_limite(id_usuario, id_libro, fecha_limite):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE lecturas SET fecha_limite = %s
        WHERE id_usuario = %s AND id_libro = %s
    """, (fecha_limite, id_usuario, id_libro))
    conexion.commit()
    cursor.close()
    conexion.close()


def guardar_notas_lectura(id_lectura, respuestas):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO notas_lectura 
        (id_lectura, como_te_sientes, que_aprendiste, palabras_nuevas, personaje_destacado, 
         escena_impacto, continuara, parecer_sesion, recuerdo_vida, notas_observaciones, 
         buscaba_al_leer, encontro_lo_buscado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (id_lectura, *respuestas))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_lectura_en_progreso(id_usuario, id_libro):
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

def obtener_libro_completo(id_google=None, key_libro=None):
    print("BUSCANDO EN BD - id_google:", id_google, "key_libro:", key_libro)
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    if id_google:
        cursor.execute("""
            SELECT * FROM libros WHERE id_google = %s LIMIT 1
        """, (id_google,))
    elif key_libro:
        cursor.execute("""
            SELECT * FROM libros WHERE key_libro = %s LIMIT 1
        """, (key_libro,))
    else:
        return None
    
    libro = cursor.fetchone()
    print("RESULTADO BD:", libro)
    cursor.close()
    conexion.close()
    return libro