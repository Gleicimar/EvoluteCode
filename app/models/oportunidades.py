from datetime  import datetime
from app import db

colecao = db.oportunidades  # sua coleção no MongoDB

class   OportunidadeModel:
    def __init__(self, nome, email, telefone, projeto, origem, status="novo", followup=None, data =None):
        self.nome = nome
        self.email =email
        self.telefone = telefone
        self.projeto = projeto
        self.origem = origem
        self.status = status
        self.data = data
        self.followup = followup or [] 
        self.data= data or  datetime.utcnow()

    def salvar(self):
        doc =self.__dict__
        colecao.insert_one(doc)
    @staticmethod
    def listar(filtro={}):
        return list(colecao.find(filtro))
    @staticmethod
    def atualizar(oportunidade_id, novos_dados):
        colecao.update_one({"_id_":ObjectId(oportunidade_id)}, {"$set":novos_dados})
    @staticmethod
    def deletar(oportunidade_id):
        colecao.delete_one({"_id_":ObjectId(oportunidade_id)})
    @staticmethod
    def buscar_por_id(oportunidade_id):
        return colecao.find_one({"_id_":ObjectId(oportunidade_id)})
