from flask import Flask, request, make_response
from flask_cors import CORS
from config import Config

def create_app():
    # Configurar Flask para usar la carpeta 'plantillas'
    app = Flask(__name__, static_folder='../static', template_folder='../plantillas')
    CORS(app)

    # Configurar la clave secreta y configuraciones de sesión
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SESSION_COOKIE_SECURE'] = Config.SESSION_COOKIE_SECURE
    app.config['SESSION_COOKIE_HTTPONLY'] = Config.SESSION_COOKIE_HTTPONLY
    app.config['SESSION_COOKIE_SAMESITE'] = Config.SESSION_COOKIE_SAMESITE
    app.config['PERMANENT_SESSION_LIFETIME'] = Config.PERMANENT_SESSION_LIFETIME
    app.config['SESSION_REFRESH_EACH_REQUEST'] = Config.SESSION_REFRESH_EACH_REQUEST

    # Middleware para agregar headers de seguridad y caché
    @app.after_request
    def add_security_headers(response):
        # Headers para prevenir caché en páginas sensibles
        if request.endpoint and 'main.' in request.endpoint:
            # Para rutas del blueprint main (páginas protegidas)
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        
        # Headers de seguridad adicionales
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        return response

    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app 