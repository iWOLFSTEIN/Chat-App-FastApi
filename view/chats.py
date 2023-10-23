from fastapi import APIRouter
from controller import chat as chat_controller, users_rooms
from view.socket import sio

router = APIRouter()


@sio.on("get_chats")
async def chats(sid, data):
    user_id = data.get("id")
    users_rooms.rooms[user_id] = [sid, sio]
    chat_data = chat_controller.get_all_chats(user_id)
    await chat_controller.send_chat_data(sio, chat_data=chat_data, sid=sid)
