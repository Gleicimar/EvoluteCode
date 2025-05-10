from pymongo import MongoClient


conexao = MongoClient("mongodb://localhost:27017/")

db = conexao['evolutecode']

usuario  = db['usuarios']
