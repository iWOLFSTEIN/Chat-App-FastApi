from typing import Annotated
from fastapi import APIRouter, Depends
from controller.validate import oauth2_scheme
from models.message import Message
from controller import chat

router = APIRouter()

@router.post("/chat/{sender_id}")
async def send_message(
        sender_id: str, 
        message: Message, 
        token: Annotated[str, Depends(oauth2_scheme)]
        ):
    return chat.send_message(sender_id=sender_id, message=message, token=token)

