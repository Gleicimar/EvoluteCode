from flask import Flask
from config import Config
from flask_talisman import Talisman
from flask_wtf import CSRFProtect
csrf =CSRFProtect()
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ='login'

def create_app():
    app = Flask(__name__)
    talisman = Talisman(app, content_security_policy=None)
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
    csrf.init_app(app)
    from  .routes.auth_routes import auth
    from .routes.routes import main

    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app