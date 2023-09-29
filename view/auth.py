from fastapi import APIRouter
from models.login_form import LoginForm
from models.user import User

router = APIRouter()

@router.get("/login") 
async def login(login_form: LoginForm): 
    return {"user": login_form, "message": "Login successful!"}

@router.post("/signup")
async def signup(user: User):
    return {"user": user, 'message': "Signup successful!"}