from app.models.mongo import db
from bson import ObjectId

def inserir_projeto(projeto):
    return db.projetos.insert_one(projeto)

def listar_projetos():
    return list(db.projetos.find({}))

def buscar_projeto(projeto_id):
    return db.projetos.find_one({'_id': ObjectId(projeto_id)})

def atualizar_projeto(projeto_id, dados):
    return db.projetos.update_one({'_id': ObjectId(projeto_id)}, {'$set': dados})

def remover_projeto(projeto_id):
    return db.projetos.delete_one({'_id': ObjectId(projeto_id)})
