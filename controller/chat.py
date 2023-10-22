import asyncio
import pymongo
from controller.mongo_db import MongoCollections, MongoStore
from controller.validate import check_token_validity
from models.chat import Chat
from models.message import Message
import hashlib
from controller import users_rooms

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
async def send_message(sender_id: str, message: Message):
    db = MongoStore.mongo_db()
    participants = order_strings_ascending_in_place([sender_id, message.receiver_id])
    key = generate_consistent_key(participants)

    chat_sender = Chat(
        **{"owner": sender_id, "last_message": message, "room_id": key}
    ).dict()
    chat_receiver = Chat(
        **{"owner": message.receiver_id, "last_message": message, "room_id": key}
    ).dict()
    room = Room(**{"room_id": key, "message": message, "participants": participants})

    db[MongoCollections.chats].replace_one(
        filter={"owner": sender_id, "room_id": key},
        replacement=chat_sender,
        upsert=True,
    )
    db[MongoCollections.chats].replace_one(
        filter={"owner": message.receiver_id, "room_id": key},
        replacement=chat_receiver,
        upsert=True,
    )
    db[MongoCollections.rooms].insert_one(room.dict())

    sender_socket = users_rooms.rooms.get(sender_id)
    receiver_socket = users_rooms.rooms.get(message.receiver_id)
    asyncio.gather(
        send_data_if_exists(sender_id, sender_socket, chat_sender),
        send_data_if_exists(message.receiver_id, receiver_socket, chat_receiver),
    )

    return room


async def send_data_if_exists(id, socket, chat_data):
    if socket:
        try:
            chat_data = get_all_chats(id)
            await send_chat_data(socket[1], chat_data=chat_data, sid=socket[0])
        except ():
            pass


def get_all_chats(id: str):
    db = MongoStore.mongo_db()
    result = (
        db[MongoCollections.chats]
        .find({"owner": id})
        .sort("last_message.timestamp", pymongo.ASCENDING)
    )

    chats = []
    for chat in result:
        chat_dict = Chat(**chat).dict()
        chat_dict["last_message"]["timestamp"] = chat_datetime_to_json(chat_dict)

        chats.append(chat_dict)

    return chats


async def send_chat_data(sio, chat_data: dict, sid: str):
    await sio.emit("chats", chat_data, room=sid)


def chat_datetime_to_json(chat_dict) -> dict:
    return chat_dict["last_message"]["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")
