import os
from pymongo import MongoClient
from config import Config
from gridfs import GridFS

MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
  raise ValueError("Variável MONGO_URI não está definida")
print("Conectado com sucesso")


conexao = MongoClient(MONGO_URI)
db = conexao['evolutecode']

usuario  = db['usuarios']
projetos = db['projetos']
crm_oportubidades = db['crm_oportunidades']
fs = GridFS(db)
