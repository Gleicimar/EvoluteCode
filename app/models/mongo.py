from pymongo import MongoClient


conexao = MongoClient("mongodb+srv://gleicimarribeiro:271121Gl@cluster0.oxswoxj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = conexao['evolutecode']

usuario  = db['usuarios']
