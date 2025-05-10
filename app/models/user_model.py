from .mongo import  db

def autenticar_usuario(usuario,senha):
    return db.usuarios.find_one({"usuario":usuario,"senha":senha})

def cadastrar_usuario(usuario,senha):
    db.usuarios.insert_one({"usuario":usuario,"senha":senha})
    
def atualizar_usuario(usuario,senha):
    db.usuarios.update_one({"usuario":usuario},{"$set":{"senha":senha}})
