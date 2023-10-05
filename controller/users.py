from controller.mongo_db import MongoCollections, MongoStore
from controller.token_validity import check_token_validity
from models.user import User

@check_token_validity
def get_users(max_limit: int):
    db = MongoStore().mongo_db()
    result = db[MongoCollections.users].find().limit(max_limit)
    users = [User(**user) for user in result]
    return users

@check_token_validity
def get_single_user(id: str) -> User | None:
    db = MongoStore().mongo_db()
    user = db[MongoCollections.users].find_one({'_id': id})
    if user:
        return User(**user)
    return None