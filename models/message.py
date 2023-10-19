from pydantic import BaseModel, Field
from datetime import datetime


class Message(BaseModel):
    receiver_id: str
    message: str
    timestamp: datetime = Field(...)

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime("%Y-%m-%dT%H:%M:%S")
