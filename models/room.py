from pydantic import BaseModel

from models import message
from typing import List


class Room(BaseModel):
    room_id: str
    message: message.Message
    participants: List[str]