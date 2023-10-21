from fastapi import FastAPI
from view import auth, chats, users
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chats.router)
app.mount("/", app=chats.app)
