from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_key'
    app.config.from_object(Config)
     # Segurança
    @app.after_request
    def set_secure_headers(response):
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    from  .routes.auth_routes import auth
    from .routes.routes import main

    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app