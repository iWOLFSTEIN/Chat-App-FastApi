from pydantic import BaseModel
from models.message import Message

class Chat(BaseModel):
    owner: str
    last_message: Message
    room_id: str

    class Config:
        arbitrary_types_allowed = True
        


    