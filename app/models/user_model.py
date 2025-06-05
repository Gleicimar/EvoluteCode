from passlib.hash import bcrypt
from flask_login import UserMixin
from flask import flash
from .mongo import db

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.usuario = user_data.get('usuario')

    def get_id(self):
        return self.id

def autenticar_usuario(usuario, senha):
    usuario_data = db.usuarios.find_one({"usuario": usuario})
    if usuario_data:
        if bcrypt.verify(senha, usuario_data["senha"]):
            return usuario_data
    flash("Usuário ou senha incorretos", 'error')
    return None

def cadastrar_usuario(usuario, senha):
    if db.usuarios.find_one({"usuario": usuario}):
        flash("Usuário já cadastrado", "error")
        return False
    senha_hash = bcrypt.hash(senha)
    db.usuarios.insert_one({"usuario": usuario, "senha": senha_hash})
    return True

def atualizar_usuario(usuario, nova_senha):
    senha_hash = bcrypt.hash(nova_senha)
    resultado = db.usuarios.update_one({"usuario": usuario}, {"$set": {"senha": senha_hash}})
    return resultado.modified_count > 0
