from flask import Flask
from app.models.mongo import conexao

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_key'
    from  .routes.auth_routes import auth
    from .routes.routes import main
    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app