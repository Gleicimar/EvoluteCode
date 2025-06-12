import os
from pymongo import MongoClient
from config import Config

MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
  raise ValueError("Variável MONGO_URI não está definida")
print("Conectado com sucesso")



conexao = MongoClient(MONGO_URI)
db = conexao['evolutecode']

usuario  = db['usuarios']
projetos = db['projetos']
