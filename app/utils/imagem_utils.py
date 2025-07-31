from app.models.mongo import fs
from bson import ObjectId
from werkzeug.utils import secure_filename

def salvar_imagem(imagem):
    return fs.put(imagem, filename=secure_filename(imagem.filename))

def deletar_imagem(imagem_id):
    return fs.delete(ObjectId(imagem_id))

def buscar_imagem(imagem_id):
    return fs.get(ObjectId(imagem_id))
