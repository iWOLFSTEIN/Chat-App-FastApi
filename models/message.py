from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    receiver_id: str
    message: str
    timestamp: datetime