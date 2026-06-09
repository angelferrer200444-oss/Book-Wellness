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

def agregar_libro(id_usuario, titulo, autor, descripcion, portada, categoria, key_libro):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT id_libro FROM libros 
        WHERE id_usuario = %s AND titulo = %s
    """, (id_usuario, titulo))
    
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        return False

    cursor.execute("""
        INSERT INTO libros (id_usuario, titulo, autor, descripcion, portada, categoria, key_libro) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (id_usuario, titulo, autor, descripcion, portada, categoria, key_libro))
    conexion.commit()
    cursor.close()
    conexion.close()
    return True

def obtener_libros_usuario(id_usuario, categoria):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_libro, titulo, autor, portada, key_libro FROM libros 
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