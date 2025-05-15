import bcrypt
from flask import flash
from .mongo import  db

def autenticar_usuario(usuario,senha):
    usuario = db.usuarios.find_one({"usuario":usuario})
    if usuario:
        senha_hash = usuario["senha"].encode('utf-8')
        if bcrypt.checkpw(senha.encode('utf-8'),senha_hash):
            return usuario
    return flash("Usuário ou senha incorretos",'error')

def cadastrar_usuario(usuario,senha):
    if db.usuarios.find_one({"usuario":usuario}):
        return False
    senha_hash =bcrypt.hashpw(senha.encode('utf-8'),bcrypt.gensalt)
    db.usuarios.insert_one({"usuario":usuario,"senha":senha_hash.decode('utf-8')})
    return True
    
def atualizar_usuario(usuario,senha):
    db.usuarios.update_one({"usuario":usuario},{"$set":{"senha":senha}})
