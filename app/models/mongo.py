from pymongo import MongoClient
from config import Config

conexao = MongoClient(MONGO_URI)
db = conexao['evolutecode']

usuario  = db['usuarios']
