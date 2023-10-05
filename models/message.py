from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    receiver_id: str
    message: str
    time_stamp: datetime