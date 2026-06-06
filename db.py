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