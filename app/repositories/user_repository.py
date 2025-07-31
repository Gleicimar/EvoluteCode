# app/repositories/user_repository.py

from app.models.mongo import db
from werkzeug.security import generate_password_hash

def buscar_usuario_por_nome(nome):
    return db.usuarios.find_one({'usuario': nome})

def criar_usuario(usuario, senha, cargo):
    if buscar_usuario_por_nome(usuario):
        return False
    senha_hash = generate_password_hash(senha)
    db.usuarios.insert_one({'usuario': usuario, 'senha': senha_hash, 'cargo': cargo})
    return True

def listar_todos_usuarios():
    return list(db.usuarios.find({}))
