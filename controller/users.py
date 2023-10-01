from controller.mongo_db import MongoCollections, MongoStore
from controller.token_validity import check_token_validity
from models.user import User

@check_token_validity
def get_users(max_limit: int):
    db = MongoStore().mongo_db()
    result = db[MongoCollections.users].find().limit(max_limit)
    users = [User(**user) for user in result]
    return users
