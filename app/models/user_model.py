from passlib.hash import bcrypt
from flask import flash
from .mongo import  db

def autenticar_usuario(usuario,senha):
    usuario = db.usuarios.find_one({"usuario":usuario})
    if usuario:
        senha_hash = usuario["senha"].encode('utf-8')
        if bcrypt.verify (senha, senha_hash):
            return usuario
    flash("Usuário ou senha incorretos",'error')
    return None

def cadastrar_usuario(usuario,senha):
    if db.usuarios.find_one({"usuario":usuario}):
        return False
    senha_hash =bcrypt.hash(senha)
    db.usuarios.insert_one({"usuario":usuario,"senha":senha_hash})
    return True
    
def atualizar_usuario(usuario,senha):
      senha_hash =bcrypt.hash(senha)  
     db.usuarios.update_one({"usuario":usuario},{"$set":{"senha":senha_hash}})