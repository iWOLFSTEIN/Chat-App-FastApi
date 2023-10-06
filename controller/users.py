from bson import ObjectId
from controller.mongo_db import MongoCollections, MongoStore
from controller.validate import check_token_validity
from models.user import User

@check_token_validity
def get_users(max_limit: int):
    db = MongoStore.mongo_db()
    result = db[MongoCollections.users].find().limit(max_limit)
    users = [User(**user).dict(exclude={'password'}) for user in result]
    return users

@check_token_validity
def get_user_by_id(id: str) -> User | None:
    db = MongoStore.mongo_db()
    user = db[MongoCollections.users].find_one({'_id': ObjectId(id)})
    if user:
        return User(**user).dict(exclude={'password'})
    return None

def get_user_by_query(query: dict) -> User | None:
    print(query)
    db = MongoStore.mongo_db()
    user = db[MongoCollections.users].find_one(query)
    if user:
        return User(**user)
    return None 