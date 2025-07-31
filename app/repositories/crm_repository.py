from app.models.mongo import db

def listar_oportunidades():
    return list(db.oportunidades.find())

def contar_por_status():
    pipeline = [
        {"$group": {"_id": "$status", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}}
    ]
    return list(db.oportunidades.aggregate(pipeline))
