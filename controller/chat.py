from controller.mongo_db import MongoCollections, MongoStore
# from controller.users import get_user_by_id
from controller.validate import check_token_validity
from models.message import Message

@check_token_validity
def send_message(sender_id: str, message: Message):
    db = MongoStore.mongo_db()
    db[MongoCollections.chats].insert_one({})
    return {'sender_id': sender_id, 'message': message}