from fastapi import FastAPI
from view import auth, messages, users, chats
from view.socket import app as socket_app
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(messages.router)
app.include_router(chats.router)
app.mount("/", app=socket_app)
