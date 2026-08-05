from flask import Blueprint, request, jsonify, session
from .orquestador import OrquestadorIA

ia_bp = Blueprint("ia", __name__)

motor = OrquestadorIA()

PROMPT_SISTEMA = """
Eres AM, un asistente especializado en lectura.
Responde siempre en español.
Sé amable, claro y breve.
Tus respuestas deben tener máximo 4 líneas.
Solo responde temas relacionados con libros, lectura, hábitos lectores,
recomendaciones y productividad relacionada con la lectura.
"""


@ia_bp.route("/api/ia", methods=["POST"])
def preguntar_ia():

    datos = request.get_json()

    mensaje = datos.get("mensaje", "").strip()

    if "id_usuario" not in session:

        return jsonify({
            "respuesta": "Debes iniciar sesión."
        })

    if not mensaje:
        return jsonify({
            "respuesta": "Escribe una pregunta."
        })

    try:

        id_usuario = session["id_usuario"]

        respuesta = motor.generar_texto(

            id_usuario,

            PROMPT_SISTEMA,

            mensaje

        )

    except Exception as e:


        respuesta = f"Error: {e}"


    return jsonify({
        "respuesta": respuesta
    })

