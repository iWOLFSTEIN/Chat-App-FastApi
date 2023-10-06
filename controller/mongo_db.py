from pymongo import MongoClient
from config import DATABASE_NAME, MONGO_DB_URL

class MongoStore:
    _db_instance = None

    @staticmethod
    def db_connect() -> MongoClient:
        client = MongoClient(MONGO_DB_URL)
        return client
    
    @staticmethod
    def mongo_db():
        if MongoStore._db_instance is not None:
            return MongoStore._db_instance
        db_connection = MongoStore.db_connect() 
        db = db_connection[DATABASE_NAME]
        MongoStore._db_instance = db
        return db


class MongoCollections: 
    users: str = "users"
    chats: str = "chats"
    rooms: str = "rooms"

