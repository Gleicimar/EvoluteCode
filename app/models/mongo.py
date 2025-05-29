import os
from pymongo import MongoClient
from config import Config

config=MONGO_URI



conexao = MongoClient(MONGO_URI)
db = conexao['evolutecode']

usuario  = db['usuarios']
