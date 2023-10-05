from fastapi import FastAPI
from view import auth, users, chat

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chat.router)