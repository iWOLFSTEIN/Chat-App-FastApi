from typing import Annotated
from fastapi import APIRouter, Depends
from controller.validate import oauth2_scheme, validate_token
from models.message import Message
from controller import chat as chat_controller, users_rooms
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
    return await chat_controller.send_message(
        sender_id=sender_id, message=message, token=token
    )


@sio.event
async def connect(sid, environ, auth):
    token = environ.get("HTTP_ACCESS_TOKEN")
    if not validate_token(token=token):
        socket_exception_connection_refused(ErrorMessage.invalid_token)
    print("connect ", sid)


@sio.event
async def disconnect(sid):
    print("disconnect ", sid)


@sio.on("get_chats")
async def chats(sid, data):
    user_id = data.get("id")
    users_rooms.rooms[user_id] = [sid, sio]
    # for chat_data in chat_controller.get_all_chats(user_id):
    chat_data = chat_controller.get_all_chats(user_id)
    await chat_controller.send_chat_data(sio, chat_data=chat_data, sid=sid)
