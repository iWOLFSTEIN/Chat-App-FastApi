from controller.mongo_db import MongoCollections, MongoStore
from controller.validate import check_token_validity
from models.chat import Chat
from models.message import Message
import hashlib

from models.room import Room


def order_strings_ascending_in_place(strings):
    strings.sort()
    return strings


def generate_consistent_key(strings, length=24):
    combined_string = "".join(strings)
    sha256_hash = hashlib.sha256(combined_string.encode()).hexdigest()
    truncated_hash = sha256_hash[:length]
    return truncated_hash


@check_token_validity
def send_message(sender_id: str, message: Message):
    db = MongoStore.mongo_db()
    participants = order_strings_ascending_in_place([sender_id, message.receiver_id])
    key = generate_consistent_key(participants)

    db[MongoCollections.chats].replace_one(
        filter={"owner": sender_id, "room_id": key},
        replacement=Chat(
            **{"owner": sender_id, "last_message": message, "room_id": key}
        ).dict(),
        upsert=True,
    )

    db[MongoCollections.chats].replace_one(
        filter={"owner": message.receiver_id, "room_id": key},
        replacement=Chat(
            **{"owner": message.receiver_id, "last_message": message, "room_id": key}
        ).dict(),
        upsert=True,
    )

    room = Room(**{"room_id": key, "message": message, "participants": participants})
    db[MongoCollections.rooms].insert_one(room.dict())

    return room


