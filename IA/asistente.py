from flask import Blueprint, request, jsonify
import urllib.request
import json

ia_bp = Blueprint("ia", __name__)

API_KEY = "LA KEY NO SE PUBLICA"

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

    if not mensaje:
        return jsonify({
            "respuesta": "Escribe una pregunta."
        })

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={API_KEY}"
    )

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text":
                            PROMPT_SISTEMA +
                            "\n\nUsuario: " +
                            mensaje
                    }
                ]
            }
        ]
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(req) as response:

            resultado = json.loads(
                response.read().decode("utf-8")
            )

        respuesta = resultado["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:

        respuesta = f"Error: {e}"

    return jsonify({
        "respuesta": respuesta
    })
