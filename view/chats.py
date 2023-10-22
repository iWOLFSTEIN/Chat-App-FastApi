from typing import Annotated
from fastapi import APIRouter, Depends
from controller.validate import oauth2_scheme
from models.message import Message
from controller import chat as chat_controller, users_rooms
from view.socket import sio


router = APIRouter()


@router.post("/chat/{sender_id}")
async def send_message(
    sender_id: str, message: Message, token: Annotated[str, Depends(oauth2_scheme)]
):
    return await chat_controller.send_message(
        sender_id=sender_id, message=message, token=token
    )


@sio.on("get_chats")
async def chats(sid, data):
    user_id = data.get("id")
    users_rooms.rooms[user_id] = [sid, sio]
    chat_data = chat_controller.get_all_chats(user_id)
    await chat_controller.send_chat_data(sio, chat_data=chat_data, sid=sid)
