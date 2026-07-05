from flask import Flask
from flask_cors import CORS

# Importar las rutas
from routes.home import registrar_rutas as home_routes
from routes.libros import registrar_rutas as libros_routes
from routes.usuarios import registrar_rutas as usuarios_routes
from routes.lectura import registrar_rutas as lectura_routes
from routes.seguimiento import registrar_rutas as seguimiento_routes
from IA.recomendador import recomendador_bp

from IA.asistente import ia_bp

app = Flask(__name__)

app.secret_key = "ilovesucklemons" # clave secretosa

app.register_blueprint(ia_bp)

app.register_blueprint(recomendador_bp)

CORS(app)

# Registrar todas las rutas
home_routes(app)
libros_routes(app)
usuarios_routes(app)
lectura_routes(app)
seguimiento_routes(app)

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
