from app.models.mongo import db
from bson import ObjectId

def listar_oportunidades():
    return list(db.oportunidades.find({}))

def buscar_oportunidade(id):
    return db.oportunidades.find_one({'_id': ObjectId(id)})

def atualizar_oportunidade(id, dados):
    return db.oportunidades.update_one({'_id': ObjectId(id)}, {'$set': dados})

def deletar_oportunidade(id):
    result = db.oportunidades.delete_one({'_id': ObjectId(id)})
    return result.deleted_count == 1

def remover_followup(id, followup_id):
    return db.oportunidades.update_one(
        {'_id': ObjectId(id)},
        {'$pull': {'followup': {'_id': ObjectId(followup_id)}}}
    )

def atualizar_followup(id, followup_id, descricao, autor, data):
    return db.oportunidades.update_one(
        {'_id': ObjectId(id), 'followup._id': ObjectId(followup_id)},
        {'$set': {
            'followup.$.descricao': descricao,
            'followup.$.autor': autor,
            'followup.$.data': data
        }}
    )

def adicionar_followup(id, followup):
    return db.oportunidades.update_one(
        {'_id': ObjectId(id)},
        {'$push': {'followup': followup}}
    )
