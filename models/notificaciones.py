import sys
import os
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Blueprint, jsonify, session

# Importación flexible de Calendario según el entorno de ejecución
try:
    from .calendario import Calendario
except (ImportError, ModuleNotFoundError):
    try:
        from calendario import Calendario
    except (ImportError, ModuleNotFoundError):
        DIR_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if DIR_RAIZ not in sys.path:
            sys.path.insert(0, DIR_RAIZ)
        from calendario import Calendario

# ==========================================
# BLUEPRINT DE FLASK PARA NOTIFICACIONES
# ==========================================
notificaciones_bp = Blueprint('notificaciones', __name__)

@notificaciones_bp.route('/notificaciones/estado', methods=['GET'])
def estado_notificaciones():
    """Consulta si el usuario tiene activas las notificaciones en su sesión."""
    estado_actual = session.get('notificaciones_activas', True)
    return jsonify({'activadas': estado_actual}), 200


@notificaciones_bp.route('/notificaciones/toggle', methods=['POST'])
def toggle_notificaciones():
    """Alterna el estado del botón de notificaciones en la sesión del usuario."""
    estado_actual = session.get('notificaciones_activas', True)
    nuevo_estado = not estado_actual
    session['notificaciones_activas'] = nuevo_estado
    return jsonify({'activadas': nuevo_estado}), 200


@notificaciones_bp.route('/notificaciones/ejecutar-ahora')
def ejecutar_notificaciones_ahora():
    """Ejecuta inmediatamente el envío de notificaciones del día para todos los usuarios."""
    try:
        procesar_notificaciones_diarias()
        return "✅ Notificaciones procesadas y enviadas para todos los usuarios con actividades hoy.", 200
    except Exception as e:
        return f"❌ Error ejecutando notificaciones: {e}", 500


@notificaciones_bp.route('/notificaciones/ejecutar-usuario/<int:id_usuario>')
def ejecutar_notificacion_usuario(id_usuario):
    """Ejecuta el proceso del día de hoy para un único usuario mediante su ID."""
    hoy = date.today().strftime('%Y-%m-%d')
    usuarios_notificar = Calendario.obtener_actividades_usuarios_por_fecha(hoy)

    if not usuarios_notificar:
        return f"⚠️ No hay actividades programadas para ningún usuario hoy ({hoy}).", 200

    usuario = next((u for u in usuarios_notificar if u.get('id_usuario') == id_usuario), None)

    if not usuario:
        return f"⚠️ El usuario ID {id_usuario} no tiene actividades programadas para hoy ({hoy}).", 404

    # Verificar si tiene las notificaciones activadas
    notif_activas_sesion = session.get('notificaciones_activas', True) if session else True
    if not notif_activas_sesion or not usuario.get('notificaciones_activas', True):
        return f"🔕 Notificación omitida: El usuario {usuario['nombre']} tiene las notificaciones desactivadas.", 200

    exito = _construir_y_enviar_correo_usuario(usuario, hoy)

    if exito:
        return f"✅ Notificación enviada con éxito a {usuario['nombre']} ({usuario['correo']}).", 200
    return f"❌ Error al enviar el correo a {usuario['correo']}.", 500


@notificaciones_bp.route('/notificaciones/enviar-reporte-hoy/<string:correo>')
def enviar_reporte_hoy_correo(correo):
    """Ejecuta el proceso del día de hoy para un único usuario mediante su correo."""
    hoy = date.today().strftime('%Y-%m-%d')
    usuarios_notificar = Calendario.obtener_actividades_usuarios_por_fecha(hoy)

    if not usuarios_notificar:
        return f"⚠️ No hay actividades registradas en el calendario para hoy ({hoy}).", 200

    usuario = next((u for u in usuarios_notificar if u['correo'].lower() == correo.lower()), None)

    if not usuario:
        return f"⚠️ El correo '{correo}' no tiene actividades programadas para hoy ({hoy}).", 404

    exito = _construir_y_enviar_correo_usuario(usuario, hoy)

    if exito:
        return f"✅ Reporte diario enviado a {usuario['nombre']} ({correo}).", 200
    return f"❌ Error enviando correo a {correo}.", 500

# ==========================================
# CONFIGURACIÓN DE GMAIL Y ENVÍO DE CORREOS
# ==========================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
CORREO_EMISOR = "bookwellnesscontacto@gmail.com"
PASSWORD_EMISOR = "elrv wdvx wbhv oeep"  # Contraseña de aplicación de Gmail


def enviar_correo(destinatario, asunto, cuerpo):
    """Envía un correo electrónico mediante smtplib."""
    msg = MIMEMultipart()
    msg['From'] = f"Book Wellness <{CORREO_EMISOR}>"
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(CORREO_EMISOR, PASSWORD_EMISOR)
        server.send_message(msg)
        server.quit()
        print(f"[NOTIFICACIÓN] Correo enviado exitosamente a: {destinatario}")
        return True
    except Exception as e:
        print(f"[ERROR NOTIFICACIÓN] No se pudo enviar el correo a {destinatario}: {e}")
        return False


def _construir_y_enviar_correo_usuario(usuario, fecha_str):
    """Función auxiliar interna para armar la plantilla y enviar el correo."""
    nombre = usuario['nombre']
    correo = usuario['correo']
    eventos = usuario['eventos']

    cuerpo = f"Hola {nombre},\n\nTienes actividades o metas marcadas en tu calendario de Book Wellness para hoy ({fecha_str}):\n\n"
    for ev in eventos:
        if ev['tipo'] == 'fin_libro':
            cuerpo += f"  • ⏰ Fecha límite para terminar: {ev['titulo']}\n"
        elif ev['tipo'] == 'sesion':
            cuerpo += f"  • 📖 Sesión de lectura programada: {ev['titulo']}\n"

    cuerpo += "\n¡Te deseamos una excelente sesión de lectura hoy!\n\nAtentamente,\nEl equipo de Book Wellness"
    asunto = f"📚 Book Wellness - Tus actividades de hoy ({fecha_str})"

    return enviar_correo(correo, asunto, cuerpo)


def procesar_notificaciones_diarias():
    """Consulta MySQL y envía las notificaciones diarias reales a todos los usuarios correspondientes."""
    hoy = date.today().strftime('%Y-%m-%d')
    print(f"\n[INICIO] Buscando actividades para la fecha: {hoy}...")

    # Consultar estado en sesión si existe contexto de Flask
    try:
        notif_activas_sesion = session.get('notificaciones_activas', True)
    except RuntimeError:
        notif_activas_sesion = True

    # CORRECCIÓN: Se usa el método correcto definido en Calendario
    usuarios_notificar = Calendario.obtener_actividades_usuarios_por_fecha(hoy)

    if not usuarios_notificar:
        print("[NOTIFICACIÓN] No hay actividades o fechas límite registradas para el día de hoy.")
        return

    for u in usuarios_notificar:
        if not notif_activas_sesion or not u.get('notificaciones_activas', True):
            print(f"[NOTIFICACIÓN] Omitiendo envío a {u.get('correo')}: Notificaciones desactivadas.")
            continue

        _construir_y_enviar_correo_usuario(u, hoy)

# ==========================================
# INICIALIZADOR EN SEGUNDO PLANO (FLASK)
# ==========================================
scheduler_instancia = None

def iniciar_scheduler_background():
    """Inicia el temporizador de notificaciones en segundo plano a las 08:00 AM al arrancar Flask."""
    global scheduler_instancia
    
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not os.environ.get('FLASK_RUN_FROM_CLI'):
        if scheduler_instancia is None:
            scheduler_instancia = BackgroundScheduler()
            scheduler_instancia.add_job(
                procesar_notificaciones_diarias, 
                'cron', 
                hour=8, 
                minute=0, 
                id='notificaciones_diarias_job',
                replace_existing=True
            )
            scheduler_instancia.start()
            print("[SISTEMA] Servicio de notificaciones programado en segundo plano (Diario a las 08:00 AM).")

# ==========================================
# MODO DE EJECUCIÓN DIRECTA
# ==========================================
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "hoy":
        procesar_notificaciones_diarias()
    else:
        print("Iniciando servicio automático de notificaciones independiente...")
        scheduler = BlockingScheduler()
        scheduler.add_job(procesar_notificaciones_diarias, 'cron', hour=8, minute=0)
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            print("\nServicio de notificaciones detenido.")