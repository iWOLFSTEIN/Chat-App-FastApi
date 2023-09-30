from fastapi import APIRouter
from controller.auth import create_user, login_user
from models.login_form import LoginForm
from models.user import User

router = APIRouter()

@router.get("/login") 
async def login(login_form: LoginForm): 
    return login_user(login_form=login_form)

@router.post("/signup")
async def signup(user: User):
    return create_user(user=user)