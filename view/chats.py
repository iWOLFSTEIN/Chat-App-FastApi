from typing import Annotated
from fastapi import APIRouter, Depends
from controller.validate import oauth2_scheme
from models.message import Message
from controller import chat as chat_controller
import socketio

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
    print("connect ", sid)


@sio.event
async def disconnect(sid):
    print("disconnect ", sid)


@sio.on("chats")
async def chats(sid, data):
    await sio.emit("users", {sid: "chat data"})
