import asyncio
import hashlib

import pymongo
from controller.chat import get_all_chats, send_chat_data
from controller.mongo_db import MongoCollections, MongoStore
from controller.validate import check_token_validity
from models.chat import Chat

from models.message import Message
from models.room import Room
from controller import users_rooms


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
    room_socket = users_rooms.rooms.get(key)

    asyncio.gather(
        send_chat_if_exists(sender_id, sender_socket),
        send_chat_if_exists(message.receiver_id, receiver_socket),
        send_message_if_exists(key, room_socket),
    )

    return room


async def send_chat_if_exists(id, socket):
    if socket:
        try:
            chat_data = get_all_chats(id)
            await send_chat_data(socket[1], chat_data=chat_data, sid=socket[0])
        except ():
            pass


async def send_message_if_exists(id, socket):
    if socket:
        try:
            print("Room id in send message if exist " , id)
            user_messages = get_all_messages(room_id=id)
            await send_messages_data(socket[1], message=user_messages, sid=id)
        except ():
            pass


def get_all_messages(room_id: str):
    db = MongoStore.mongo_db()
    result = (
        db[MongoCollections.rooms]
        .find({"room_id": room_id})
        .sort("message.timestamp", pymongo.ASCENDING)
    ).limit(1000)

    messages = []
    for message in result:
        message_dict = Room(**message).dict()
        message_dict["message"]["timestamp"] = message_datetime_to_json(message_dict)

        messages.append(message_dict)

    return messages


def message_datetime_to_json(dict) -> dict:
    return dict["message"]["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")


async def send_messages_data(sio, messages: dict, sid: str):
    await sio.emit("messages", messages, room=sid)

