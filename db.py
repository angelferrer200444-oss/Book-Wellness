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

def agregar_libro(id_usuario, titulo, autor, descripcion, portada, categoria, key_libro, paginas, id_google=None, genero=None, anio=None, es_manual=False, formato=None):
    if portada and isinstance(portada, str) and portada.startswith("http://"):
        portada = portada.replace("http://", "https://", 1)

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
        INSERT INTO libros (id_usuario, titulo, autor, descripcion, portada, categoria, key_libro, paginas_totales, id_google, genero, anio, es_agregado_manualmente, formato) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (id_usuario, titulo, autor, descripcion, portada, categoria, key_libro, paginas, id_google, genero, anio, es_manual, formato))
    conexion.commit()
    id_nuevo = cursor.lastrowid
    cursor.close()
    conexion.close()
    return id_nuevo

def obtener_libros_usuario(id_usuario, categoria):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_libro, titulo, autor, portada, key_libro, id_google, es_agregado_manualmente FROM libros 
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


def guardar_notas_lectura(
    id_lectura,
    como_te_sientes,
    continuara,
    notas,
    tipo_reflexion,
    respuesta_reflexion
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO notas_lectura
        (
            id_lectura,
            como_te_sientes,
            continuara,
            notas_observaciones,
            tipo_reflexion,
            respuesta_reflexion
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        id_lectura,
        como_te_sientes,
        continuara,
        notas,
        tipo_reflexion,
        respuesta_reflexion
    ))

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

def actualizar_progreso_lectura(id_usuario, id_libro, pagina_actual, capitulos_leidos, fecha_inicio=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_lectura FROM lecturas 
        WHERE id_usuario = %s AND id_libro = %s
    """, (id_usuario, id_libro))
    existente = cursor.fetchone()

    if existente:
        campos = "pagina_actual = %s, capitulos_leidos = %s"
        valores = [pagina_actual, capitulos_leidos]

        if fecha_inicio:
            campos += ", fecha_inicio = %s"
            valores.append(fecha_inicio)

        valores.extend([id_usuario, id_libro])
        cursor.execute(f"""
            UPDATE lecturas SET {campos}
            WHERE id_usuario = %s AND id_libro = %s
        """, valores)
    else:
        cursor.execute("""
            INSERT INTO lecturas (id_usuario, id_libro, pagina_actual, capitulos_leidos, fecha_inicio)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_usuario, id_libro, pagina_actual, capitulos_leidos, fecha_inicio))

    conexion.commit()
    cursor.close()
    conexion.close()

def guardar_recomendaciones(id_usuario, libros):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Borrar recomendaciones anteriores
    cursor.execute("DELETE FROM recomendaciones_cache WHERE id_usuario = %s", (id_usuario,))
    
    # Insertar nuevas
    for libro in libros:
        cursor.execute("""
            INSERT INTO recomendaciones_cache 
            (id_usuario, titulo, autor, descripcion, portada, paginas, generos, anio, id_google)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            id_usuario,
            libro.get('titulo'),
            libro.get('autor'),
            libro.get('descripcion'),
            libro.get('portada'),
            libro.get('paginas'),
            libro.get('generos'),
            libro.get('anio'),
            libro.get('id_google')
        ))
    
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_recomendaciones_cache(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM recomendaciones_cache 
        WHERE id_usuario = %s
        ORDER BY fecha_generacion DESC
    """, (id_usuario,))
    libros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return libros


def invalidar_cache_recomendaciones(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "DELETE FROM recomendaciones_cache WHERE id_usuario = %s",
        (id_usuario,)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_perfil_lectura(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Páginas y tiempo total
    cursor.execute("""
        SELECT 
            COALESCE(SUM(paginas_leidas), 0) as total_paginas,
            COALESCE(SUM(tiempo_minutos), 0) as total_minutos
        FROM lecturas 
        WHERE id_usuario = %s
    """, (id_usuario,))
    totales = cursor.fetchone()

    # Libros terminados
    cursor.execute("""
        SELECT COUNT(*) as libros_leidos FROM lecturas 
        WHERE id_usuario = %s AND estado = 'Terminé'
    """, (id_usuario,))
    leidos = cursor.fetchone()

    # Estado de ánimo más frecuente
    cursor.execute("""
        SELECT nl.como_te_sientes, COUNT(*) as freq
        FROM notas_lectura nl
        JOIN lecturas l ON nl.id_lectura = l.id_lectura
        WHERE l.id_usuario = %s AND nl.como_te_sientes IS NOT NULL
        GROUP BY nl.como_te_sientes
        ORDER BY freq DESC
        LIMIT 1
    """, (id_usuario,))
    animo = cursor.fetchone()

    # Géneros preferidos
    cursor.execute("""
        SELECT genero FROM libros
        WHERE id_usuario = %s AND genero IS NOT NULL AND genero != ''
    """, (id_usuario,))
    filas_generos = cursor.fetchall()

    # Contar géneros individuales
    from collections import Counter
    contador = Counter()
    for fila in filas_generos:
        for g in fila['genero'].split(','):
            g = g.strip()
            if g:
                contador[g] += 1
    generos_top = [g for g, _ in contador.most_common(3)]

    # Rachas — días con sesión registrada
    cursor.execute("""
        SELECT DISTINCT DATE(fecha_fin) as dia
        FROM lecturas
        WHERE id_usuario = %s AND fecha_fin IS NOT NULL
        ORDER BY dia ASC
    """, (id_usuario,))
    dias = [row['dia'] for row in cursor.fetchall()]

    from datetime import date, timedelta

    racha_actual = 0
    racha_maxima = 0
    racha_temp = 1

    if dias:
        # Racha máxima
        for i in range(1, len(dias)):
            if (dias[i] - dias[i-1]).days == 1:
                racha_temp += 1
                racha_maxima = max(racha_maxima, racha_temp)
            else:
                racha_temp = 1
        racha_maxima = max(racha_maxima, racha_temp)

        # Racha actual
        hoy = date.today()
        if dias[-1] == hoy or dias[-1] == hoy - timedelta(days=1):
            racha_actual = 1
            for i in range(len(dias)-1, 0, -1):
                if (dias[i] - dias[i-1]).days == 1:
                    racha_actual += 1
                else:
                    break

    cursor.close()
    conexion.close()

    return {
        "total_paginas": totales['total_paginas'],
        "total_minutos": totales['total_minutos'],
        "libros_leidos": leidos['libros_leidos'],
        "animo": animo['como_te_sientes'] if animo else "Sin datos",
        "generos_top": generos_top,
        "racha_actual": racha_actual,
        "racha_maxima": racha_maxima
    }


def obtener_fechas_calendario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT DATE(fecha_inicio) as fecha, 'sesion' as tipo
        FROM lecturas
        WHERE id_usuario = %s AND fecha_inicio IS NOT NULL
        UNION
        SELECT DATE(fecha_limite) as fecha, 'fin_libro' as tipo
        FROM lecturas
        WHERE id_usuario = %s AND fecha_limite IS NOT NULL
    """, (id_usuario, id_usuario))

    filas = cursor.fetchall()
    cursor.close()
    conexion.close()

    fechas = {}
    for fila in filas:
        fecha_str = str(fila['fecha'])
        if fecha_str not in fechas:
            fechas[fecha_str] = fila['tipo']
        elif fila['tipo'] == 'fin_libro':
            fechas[fecha_str] = 'fin_libro'

    return fechas

def obtener_eventos_por_fecha(id_usuario, fecha):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Sesiones iniciadas en esa fecha
    cursor.execute("""
        SELECT l.titulo, l.autor, l.portada, l.id_libro,
               lec.paginas_leidas, lec.tiempo_minutos,
               lec.fecha_inicio, lec.capitulos_leidos,
               'sesion' as tipo
        FROM lecturas lec
        JOIN libros l ON lec.id_libro = l.id_libro
        WHERE lec.id_usuario = %s AND DATE(lec.fecha_inicio) = %s
    """, (id_usuario, fecha))
    sesiones = cursor.fetchall()

    # Fechas límite en ese día
    cursor.execute("""
        SELECT l.titulo, l.autor, l.portada, l.id_libro,
               lec.fecha_limite, lec.estado,
               'fecha_limite' as tipo
        FROM lecturas lec
        JOIN libros l ON lec.id_libro = l.id_libro
        WHERE lec.id_usuario = %s AND DATE(lec.fecha_limite) = %s
    """, (id_usuario, fecha))
    limites = cursor.fetchall()

    cursor.close()
    conexion.close()
    return sesiones + limites

def obtener_notas_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    # Notas manuales
    cursor.execute("""
        SELECT n.id_nota, n.id_libro, n.titulo, n.contenido, n.categoria, n.fecha_creacion,
               l.titulo as libro_titulo, l.autor as libro_autor, l.portada,
               'manual' as tipo
        FROM notas_usuario n
        LEFT JOIN libros l ON n.id_libro = l.id_libro
        WHERE n.id_usuario = %s
        ORDER BY n.fecha_creacion DESC
    """, (id_usuario,))
    notas_manuales = cursor.fetchall()

    # Notas de sesión
    cursor.execute("""
        SELECT nl.id_nota, nl.como_te_sientes, nl.que_aprendiste, nl.palabras_nuevas,
               nl.personaje_destacado, nl.escena_impacto, nl.parecer_sesion,
               nl.recuerdo_vida, nl.notas_observaciones, nl.buscaba_al_leer,
               nl.encontro_lo_buscado, nl.tipo_reflexion, nl.respuesta_reflexion,
               lec.fecha_fin as fecha_creacion,
               l.id_libro, l.titulo as libro_titulo, l.autor as libro_autor, l.portada,
               'sesion' as tipo
        FROM notas_lectura nl
        JOIN lecturas lec ON nl.id_lectura = lec.id_lectura
        JOIN libros l ON lec.id_libro = l.id_libro
        WHERE lec.id_usuario = %s AND lec.fecha_fin IS NOT NULL
        ORDER BY lec.fecha_fin DESC
    """, (id_usuario,))
    notas_sesion = cursor.fetchall()

    cursor.close()
    conexion.close()
    return notas_manuales, notas_sesion


def agregar_nota_usuario(id_usuario, id_libro, titulo, contenido, categoria):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO notas_usuario (id_usuario, id_libro, titulo, contenido, categoria, fecha_creacion)
        VALUES (%s, %s, %s, %s, %s, CURDATE())
    """, (id_usuario, id_libro, titulo, contenido, categoria))
    conexion.commit()
    id_nueva = cursor.lastrowid
    cursor.close()
    conexion.close()
    return id_nueva


def editar_nota_usuario(id_nota, titulo, contenido, categoria):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE notas_usuario SET titulo=%s, contenido=%s, categoria=%s
        WHERE id_nota=%s
    """, (titulo, contenido, categoria, id_nota))
    conexion.commit()
    cursor.close()
    conexion.close()


def eliminar_nota_usuario(id_nota):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM notas_usuario WHERE id_nota=%s", (id_nota,))
    conexion.commit()
    cursor.close()
    conexion.close()


def editar_nota_sesion(id_nota, campo, valor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    campos_permitidos = [
        'como_te_sientes', 'que_aprendiste', 'palabras_nuevas',
        'personaje_destacado', 'escena_impacto', 'parecer_sesion',
        'recuerdo_vida', 'notas_observaciones', 'respuesta_reflexion'
    ]
    if campo not in campos_permitidos:
        return
    cursor.execute(f"UPDATE notas_lectura SET {campo}=%s WHERE id_nota=%s", (valor, id_nota))
    conexion.commit()
    cursor.close()
    conexion.close()