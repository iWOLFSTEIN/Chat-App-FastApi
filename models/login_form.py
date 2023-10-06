from pydantic import BaseModel, Field

class LoginForm(BaseModel):
    username: str = Field(alias='username', default=None)
    email: str = Field(alias='email', default=None)
    password: str

        