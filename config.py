import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    if not MONGO_URI:
      raise ValueError("Variável MONGO_URI não está definida")
    print("Conectado com sucesso")