import sys
import os
from flask import Blueprint, render_template, request, redirect, url_for
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from db import obtener_conexion

# Importación flexible de enviar_correo según la ubicación del ejecutor
try:
    from .notificaciones import enviar_correo
except (ImportError, ModuleNotFoundError):
    try:
        from models.notificaciones import enviar_correo
    except (ImportError, ModuleNotFoundError):
        from notificaciones import enviar_correo

recuperacion_bp = Blueprint('recuperacion', __name__)

# Clave secreta para firmar el token
SECRET_KEY = "clave_secreta_book_wellness"
serializer = URLSafeTimedSerializer(SECRET_KEY)


@recuperacion_bp.route('/recuperar', methods=['GET', 'POST'])
def solicitar_recuperacion():
    if request.method == 'POST':
        correo = request.form.get('correo')

        # 1. Verificar si el usuario existe en MySQL
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()

        if usuario:
            # 2. Generar token firmado con el correo del usuario
            token = serializer.dumps(correo, salt='recuperar-contrasena')

            # 3. Crear enlace absoluto de confirmación
            link_recuperacion = url_for(
                'recuperacion.restablecer_contrasena',
                token=token,
                _external=True
            )

            # 4. Preparar correo electrónico
            asunto = "🔐 Book Wellness - Restablecer Contraseña"
            cuerpo = (
                f"Hola {usuario['nombre']},\n\n"
                f"Hemos recibido una solicitud para cambiar tu contraseña en Book Wellness.\n"
                f"Haz clic en el siguiente enlace para restablecerla (válido por 15 minutos):\n\n"
                f"{link_recuperacion}\n\n"
                f"Si no solicitaste este cambio, puedes ignorar este mensaje de forma segura.\n\n"
                f"Atentamente,\nEl equipo de Book Wellness"
            )

            # 5. Intentar enviar el correo
            try:
                enviar_correo(correo, asunto, cuerpo)

            except Exception as e:
                print(f"[RECUPERACIÓN] Error al enviar correo: {e}")

                return render_template(
                    'HTML SESION/ErrorEnvio.html'
                )

        # Si el correo se envió correctamente, mostrar confirmación
        return render_template('HTML SESION/CodigoEnviado.html')

    return render_template('HTML SESION/¿OlvidasteContrasena.html')


@recuperacion_bp.route('/restablecer/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(token):
    try:
        # Validar token (expira en 900 segundos / 15 minutos)
        correo = serializer.loads(
            token,
            salt='recuperar-contrasena',
            max_age=900
        )

    except (SignatureExpired, BadTimeSignature):
        return (
            "<h3>El enlace de recuperación es inválido o ha expirado. "
            "Por favor, solicita uno nuevo.</h3>",
            400
        )

    if request.method == 'POST':
        nueva_password = request.form.get('password')

        if not nueva_password:
            return "La contraseña no puede estar vacía", 400

        # Actualizar contraseña en MySQL
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "UPDATE usuarios SET password = %s WHERE correo = %s",
            (nueva_password, correo)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        # Redirigir al inicio de sesión
        return redirect('/sesion')

    return render_template(
        'HTML SESION/nuevacontraseña.html',
        token=token
    )

