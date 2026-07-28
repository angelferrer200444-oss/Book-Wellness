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

