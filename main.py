from fastapi import FastAPI
from view import auth
from view import users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)