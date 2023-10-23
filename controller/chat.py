import pymongo
from controller.mongo_db import MongoCollections, MongoStore
from models.chat import Chat
from view.socket import sio


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


async def send_chat_data(chat_data: dict, sid: str):
    await sio.emit("chats", chat_data, room=sid)


def chat_datetime_to_json(chat_dict) -> dict:
    return chat_dict["last_message"]["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")
