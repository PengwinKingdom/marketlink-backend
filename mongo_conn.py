import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://marketlink-mongo:27017")
DB_NAME   = os.getenv("DB_NAME", "miPrimeraDB")

_client = MongoClient(MONGO_URI)
_db = _client[DB_NAME]

def get_mongo():
    """
    Devuelve el cliente y la base de datos de MongoDB.
    Útil para healthchecks u operaciones más avanzadas.
    """
    return _client, _db

# Colección de usuarios usada por la API
usuarios_col = _db["usuarios"]
