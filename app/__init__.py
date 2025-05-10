from flask import Flask
from models.mongo import conexao
def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_key'
    
    from .routes.routes import main
    app.register_blueprint(main)
    
    return app