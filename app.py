from flask import Flask
from flask_cors import CORS

# Importar las rutas
from routes.home import registrar_rutas as home_routes
from routes.libros import registrar_rutas as libros_routes
from routes.usuarios import registrar_rutas as usuarios_routes
from routes.lectura import registrar_rutas as lectura_routes
from routes.seguimiento import registrar_rutas as seguimiento_routes
from routes.objetivos import objetivos_bp

# Importar Blueprints y el Scheduler en segundo plano
from IA.recomendador import recomendador_bp
from IA.asistente import ia_bp
from models.notificaciones import notificaciones_bp, iniciar_scheduler_background

app = Flask(__name__)

app.secret_key = "ilovesucklemons" # clave secretosa

# Registrar Blueprints
app.register_blueprint(ia_bp)
app.register_blueprint(recomendador_bp)
app.register_blueprint(notificaciones_bp)
app.register_blueprint(objetivos_bp) 

CORS(app)

# Registrar todas las rutas
home_routes(app)
libros_routes(app)
usuarios_routes(app)
lectura_routes(app)
seguimiento_routes(app)

# Iniciar el servicio de notificaciones en segundo plano
iniciar_scheduler_background()

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )