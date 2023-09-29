from pydantic import BaseModel

class User(BaseModel):
    name: str | None = None
    username: str 
    email: str
    password: str
