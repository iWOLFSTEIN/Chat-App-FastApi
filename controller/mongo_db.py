from pymongo import MongoClient
from config import DATABASE_NAME, MONGO_DB_URL

class MongoStore:
    db_instance = None

    def db_connect(self):
        client = MongoClient(MONGO_DB_URL)
        return client

    def mongo_db(self):
        if self.__class__.db_instance is not None:
            return self.__class__.db_instance
        db_connection = self.db_connect() 
        db = db_connection[DATABASE_NAME]
        self.__class__.db_instance = db
        return db


class MongoCollections: 
    users: str = "users"