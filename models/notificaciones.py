import sys
import os
import base64

from datetime import date

from email.mime.text import MIMEText

from flask import Blueprint, jsonify, session

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


# ==========================================
# IMPORTACIÓN FLEXIBLE DE MÓDULOS
# ==========================================

try:
    from .calendario import Calendario
    from .Objetivo import Objetivo
    from .Usuario import Usuario

except (ImportError, ModuleNotFoundError):

    try:
        from models.calendario import Calendario
        from models.Objetivo import Objetivo
        from models.Usuario import Usuario

    except (ImportError, ModuleNotFoundError):

        DIR_RAIZ = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        if DIR_RAIZ not in sys.path:
            sys.path.insert(0, DIR_RAIZ)

        from calendario import Calendario
        from Objetivo import Objetivo
        from Usuario import Usuario


# ==========================================
# BLUEPRINT DE FLASK PARA NOTIFICACIONES
# ==========================================

notificaciones_bp = Blueprint(
    'notificaciones',
    __name__
)


@notificaciones_bp.route(
    '/notificaciones/estado',
    methods=['GET']
)
def estado_notificaciones():

    """Consulta el estado de las notificaciones desde MySQL."""

    id_usuario = (
        session.get('usuario_id')
        or session.get('id_usuario')
    )

    if not id_usuario:
        return jsonify({
            'activadas': True
        }), 200

    activadas = Usuario.obtener_estado_notificaciones(
        id_usuario
    )

    return jsonify({
        'activadas': activadas
    }), 200


@notificaciones_bp.route(
    '/notificaciones/toggle',
    methods=['POST']
)
def toggle_notificaciones():

    """Alterna el estado de las notificaciones y lo guarda en MySQL."""

    id_usuario = (
        session.get('usuario_id')
        or session.get('id_usuario')
    )

    if not id_usuario:
        return jsonify({
            'error': 'Usuario no autenticado'
        }), 401

    estado_actual = Usuario.obtener_estado_notificaciones(
        id_usuario
    )

    nuevo_estado = not estado_actual

    Usuario.cambiar_estado_notificaciones(
        id_usuario,
        nuevo_estado
    )

    session['notificaciones_activas'] = nuevo_estado

    print(
        f"[NOTIFICACIONES] Estado actualizado a "
        f"{nuevo_estado} para el usuario ID {id_usuario}"
    )

    return jsonify({
        'activadas': nuevo_estado
    }), 200


# ==========================================
# CONFIGURACIÓN DE GMAIL API
# ==========================================

CORREO_EMISOR = os.environ.get(
    "CORREO_EMISOR",
    "bookwellnesscontacto@gmail.com"
)

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]


# ==========================================
# UBICACIÓN DEL TOKEN
# ==========================================

DIR_RAIZ = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

TOKEN_FILE = os.environ.get(
    "GMAIL_TOKEN_FILE",
    os.path.join(DIR_RAIZ, "token.json")
)


# ==========================================
# OBTENER CREDENCIALES DE GMAIL
# ==========================================

def obtener_credenciales_gmail():

    """
    Carga las credenciales guardadas en token.json.

    Si el access token expiró y existe un refresh token,
    lo renueva automáticamente.
    """

    if not os.path.exists(TOKEN_FILE):

        print(
            "[ERROR GMAIL] No se encontró token.json "
            f"en: {TOKEN_FILE}"
        )

        return None

    try:

        credenciales = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

        # Si el token expiró, se renueva automáticamente.
        if credenciales.expired:

            if credenciales.refresh_token:

                print(
                    "[GMAIL] Access token expirado. "
                    "Renovando..."
                )

                credenciales.refresh(
                    Request()
                )

                print(
                    "[GMAIL] Access token renovado correctamente."
                )

            else:

                print(
                    "[ERROR GMAIL] El token expiró "
                    "y no existe refresh token."
                )

                return None

        return credenciales

    except Exception as e:

        print(
            "[ERROR GMAIL] No se pudieron cargar "
            f"las credenciales: {e}"
        )

        return None


# ==========================================
# ENVÍO DE CORREOS MEDIANTE GMAIL API
# ==========================================

def enviar_correo(destinatario, asunto, cuerpo):

    """
    Envía un correo mediante Gmail API.

    Ya no utiliza SMTP.
    """

    try:

        print(
            f"[GMAIL] Preparando correo para: "
            f"{destinatario}"
        )

        # --------------------------------------
        # Obtener credenciales
        # --------------------------------------

        credenciales = obtener_credenciales_gmail()

        if not credenciales:

            print(
                "[ERROR GMAIL] No se pudieron obtener "
                "las credenciales."
            )

            return False


        # --------------------------------------
        # Crear servicio de Gmail
        # --------------------------------------

        servicio = build(
            "gmail",
            "v1",
            credentials=credenciales
        )


        # --------------------------------------
        # Crear mensaje
        # --------------------------------------

        mensaje = MIMEText(
            cuerpo,
            "plain",
            "utf-8"
        )

        mensaje["To"] = destinatario
        mensaje["From"] = (
            f"Book Wellness <{CORREO_EMISOR}>"
        )
        mensaje["Subject"] = asunto


        # --------------------------------------
        # Codificar mensaje
        # --------------------------------------

        mensaje_codificado = base64.urlsafe_b64encode(
            mensaje.as_bytes()
        ).decode()


        cuerpo_mensaje = {
            "raw": mensaje_codificado
        }


        # --------------------------------------
        # Enviar mediante Gmail API
        # --------------------------------------

        resultado = (
            servicio
            .users()
            .messages()
            .send(
                userId="me",
                body=cuerpo_mensaje
            )
            .execute()
        )


        # --------------------------------------
        # Confirmación
        # --------------------------------------

        print(
            f"[NOTIFICACIÓN] Correo enviado "
            f"exitosamente a: {destinatario}"
        )

        print(
            f"[GMAIL] ID del mensaje: "
            f"{resultado.get('id')}"
        )

        return True


    except Exception as e:

        print(
            "[ERROR NOTIFICACIÓN] "
            f"No se pudo enviar el correo a "
            f"{destinatario}: {e}"
        )

        return False


# ==========================================
# CONSTRUIR CORREO DE CALENDARIO
# ==========================================

def _construir_y_enviar_correo_usuario(
    usuario,
    fecha_str
):

    """Arma la plantilla del calendario y envía el correo."""

    nombre = usuario['nombre']
    correo = usuario['correo']
    eventos = usuario['eventos']


    cuerpo = (
        f"Hola {nombre},\n\n"
        f"Tienes actividades o metas marcadas en tu "
        f"calendario de Book Wellness para hoy "
        f"({fecha_str}):\n\n"
    )


    for ev in eventos:

        if ev['tipo'] == 'fin_libro':

            cuerpo += (
                f"  • ⏰ Fecha límite para terminar: "
                f"{ev['titulo']}\n"
            )

        elif ev['tipo'] == 'sesion':

            cuerpo += (
                f"  • 📖 Sesión de lectura programada: "
                f"{ev['titulo']}\n"
            )


    cuerpo += (
        "\n¡Te deseamos una excelente sesión de "
        "lectura hoy!\n\n"
        "Atentamente,\n"
        "El equipo de Book Wellness"
    )


    asunto = (
        f"📚 Book Wellness - Tus actividades de hoy "
        f"({fecha_str})"
    )


    return enviar_correo(
        correo,
        asunto,
        cuerpo
    )


# ==========================================
# DISPARADOR AL INICIAR SESIÓN
# ==========================================

def procesar_notificaciones_al_iniciar_sesion(
    id_usuario
):

    """
    Consulta MySQL y envía notificaciones
    únicamente si están activadas en BD.
    """

    # --------------------------------------
    # Comprobar estado en la base de datos
    # --------------------------------------

    if not Usuario.obtener_estado_notificaciones(
        id_usuario
    ):

        print(
            f"[NOTIFICACIÓN] El usuario ID "
            f"{id_usuario} tiene notificaciones "
            f"desactivadas. Omitiendo envío."
        )

        return


    # --------------------------------------
    # Fecha actual
    # --------------------------------------

    hoy = date.today().strftime(
        '%Y-%m-%d'
    )


    print(
        f"\n[LOGIN] Procesando notificaciones "
        f"para el usuario ID {id_usuario} "
        f"({hoy})..."
    )


    # ======================================
    # 1. NOTIFICACIONES DEL CALENDARIO
    # ======================================

    usuarios_cal = (
        Calendario
        .obtener_actividades_usuarios_por_fecha(
            hoy
        )
    )


    usuario_cal = next(
        (
            u
            for u in usuarios_cal
            if u.get('id_usuario') == id_usuario
        ),
        None
    )


    if usuario_cal:

        _construir_y_enviar_correo_usuario(
            usuario_cal,
            hoy
        )


    # ======================================
    # 2. NOTIFICACIONES DE OBJETIVOS
    # ======================================

    usuarios_obj = (
        Objetivo
        .obtener_usuarios_con_objetivos_por_vencer(
            hoy
        )
    )


    usuario_obj = next(
        (
            u
            for u in usuarios_obj
            if u.get('id_usuario') == id_usuario
        ),
        None
    )


    if usuario_obj:

        cuerpo = (
            f"Hola {usuario_obj['nombre']},\n\n"
            f"Te recordamos que hoy ({hoy}) vence "
            f"la fecha límite de tus siguientes "
            f"objetivos personales de lectura:\n\n"
        )


        for obj_titulo in usuario_obj['objetivos']:

            cuerpo += (
                f"  • 🎯 Objetivo: "
                f"{obj_titulo}\n"
            )


        cuerpo += (
            "\n¡Da el último esfuerzo para alcanzar "
            "tus metas de lectura!\n\n"
            "Atentamente,\n"
            "El equipo de Book Wellness"
        )


        asunto = (
            f"🎯 Book Wellness - ¡Hoy vence tu "
            f"objetivo de lectura! ({hoy})"
        )


        enviar_correo(
            usuario_obj['correo'],
            asunto,
            cuerpo
        )
