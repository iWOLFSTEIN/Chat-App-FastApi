from typing import Annotated
from fastapi import APIRouter, Depends

from controller.validate import oauth2_scheme
from models.message import Message
from controller import messages
from view.socket import sio


router = APIRouter()


@router.post("/text/{sender_id}")
async def send_message(
    sender_id: str, message: Message, token: Annotated[str, Depends(oauth2_scheme)]
):
    return await messages.send_message(
        sender_id=sender_id, message=message, token=token
    )


@sio.on("get_messages")
async def get_messages(sid, data):
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")

    participants = messages.order_strings_ascending_in_place([sender_id, receiver_id])
    room_id = messages.generate_consistent_key(participants)

    await sio.enter_room(sid, room_id)

    user_messages = messages.get_all_messages(room_id=room_id)
    await messages.send_messages_data(messages=user_messages, room=room_id)
