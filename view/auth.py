from fastapi import APIRouter
from controller.auth import create_user, login_user
from models.login_form import LoginForm
from models.user import User

router = APIRouter()

@router.post("/login") 
async def login(login_form: LoginForm): 
    return login_user(login_form=login_form)

@router.post("/signup")
async def signup(user: User):
    return create_user(user=user)


# @router.websocket("/chats")
# async def chats(
#     websocket: WebSocket,
#     user_id: Annotated[str, Query()],
#     token: str = Query(),
# ):
#     await websocket.accept()
#     try:
#         while True:
#             chats = get_all_chats(user_id=user_id, token=token)
#             await websocket.send_json(chats)
#             await asyncio.sleep(1)
#     except WebSocketDisconnect:
#         await websocket.close()


# @check_token_validity
# def get_all_chats(user_id: str):
#     db = MongoStore.mongo_db()
#     result = (
#         db[MongoCollections.chats]
#         .find({"owner": user_id})
#         .sort("last_message.timestamp", pymongo.ASCENDING)
#     )

#     chats = []
#     for chat in result:
#         chat_dict = Chat(**chat).dict()
#         chat_dict["last_message"]["timestamp"] = chat_dict["last_message"][
#             "timestamp"
#         ].strftime("%Y-%m-%dT%H:%M:%S")
#         chats.append(chat_dict)

#     return chats