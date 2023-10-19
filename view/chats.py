import asyncio
from typing import Annotated
from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
import pymongo
from controller.mongo_db import MongoCollections, MongoStore
from controller.validate import check_token_validity, oauth2_scheme
from models.chat import Chat
from models.message import Message
from controller import chat as chat_controller

router = APIRouter()


@router.post("/chat/{sender_id}")
async def send_message(
    sender_id: str, message: Message, token: Annotated[str, Depends(oauth2_scheme)]
):
    return chat_controller.send_message(
        sender_id=sender_id, message=message, token=token
    )


@router.websocket("/chats")
async def chats(
    websocket: WebSocket,
    user_id: Annotated[str, Query()],
    token: str = Query(),
):
    await websocket.accept()
    try:
        while True:
            chats = get_all_chats(user_id=user_id, token=token)
            await websocket.send_json(chats)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        await websocket.close()


@check_token_validity
def get_all_chats(user_id: str):
    db = MongoStore.mongo_db()
    result = (
        db[MongoCollections.chats]
        .find({"owner": user_id})
        .sort("last_message.timestamp", pymongo.ASCENDING)
    )

    chats = []
    for chat in result:
        chat_dict = Chat(**chat).dict()
        chat_dict["last_message"]["timestamp"] = chat_dict["last_message"][
            "timestamp"
        ].strftime("%Y-%m-%dT%H:%M:%S")
        chats.append(chat_dict)

    return chats
