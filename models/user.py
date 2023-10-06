from typing import Annotated
from bson import ObjectId
from pydantic import BaseModel, validator, Field

from utils.error_message import ErrorMessage

class User(BaseModel):
    id: Annotated[str | None, Field(alias='_id')] = None
    avatar: str | None = None
    name: str | None = None
    username: str 
    email: str
    password: str 

    @validator('id', pre=True, always=True)
    def validate_id(cls, value):
        try:
            ObjectId(value)
        except Exception:
            raise ValueError(ErrorMessage.invalid_object_id)
        if not value:
            return None
        return str(value)

