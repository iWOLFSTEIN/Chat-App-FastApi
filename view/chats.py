from typing import Annotated
from fastapi import APIRouter, Depends
import pymongo
from controller.mongo_db import MongoCollections, MongoStore
from controller.validate import oauth2_scheme, validate_token
from models.chat import Chat
from models.message import Message
from controller import chat as chat_controller
import socketio
from utils.error_message import ErrorMessage

from utils.exceptions import socket_exception_connection_refused

router = APIRouter()

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
app = socketio.ASGIApp(sio, socketio_path="ws")


@router.post("/chat/{sender_id}")
async def send_message(
    sender_id: str, message: Message, token: Annotated[str, Depends(oauth2_scheme)]
):
    return chat_controller.send_message(
        sender_id=sender_id, message=message, token=token
    )


@sio.event
async def connect(sid, environ, auth):
    token = environ["HTTP_AUTHORIZATION"].split(' ')[1]
    if not validate_token(token=token):
        socket_exception_connection_refused(ErrorMessage.invalid_token)
    print("connect ", sid)


@sio.event
async def disconnect(sid):
    print("disconnect ", sid)


@sio.on("chats")
async def chats(sid, data):
    for chat_data in get_all_chats(data["id"]):
        await sio.emit("users", chat_data)


def get_all_chats(id: str):
    db = MongoStore.mongo_db()
    result = (
        db[MongoCollections.chats]
        .find({"owner": id})
        .sort("last_message.timestamp", pymongo.ASCENDING)
    )

    for chat in result:
        chat_dict = Chat(**chat).dict()
        chat_dict["last_message"]["timestamp"] = chat_dict["last_message"][
            "timestamp"
        ].strftime("%Y-%m-%dT%H:%M:%S")

        yield chat_dict
