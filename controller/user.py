from datetime import datetime, timedelta
from fastapi import HTTPException
from models.login_form import LoginForm
from models.user import User
from secret import SECRET_KEY 
from config import ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS
from jose import jwt
from utils.error_message import ErrorMessage
from utils.status_codes import ALREADY_EXIST, RECORD_NOT_FOUND
from controller.mongo_db import MongoCollections, MongoStore

dummy_user_db: dict = {}

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(username: str) -> User | None:
    db = MongoStore().mongo_db()
    query = {'username': username}
    result = db[MongoCollections.users].find(query)
    users = list(result)
    if users:
        return User(**users[0])
    return None 


def create_user(user: User):
    db = MongoStore().mongo_db()
    db_user = get_user(username=user.username)
    if db_user:
        raise HTTPException(
            status_code=ALREADY_EXIST,
            detail=ErrorMessage.user_already_exist)
    db[MongoCollections.users].insert_one(user.dict())
    access_token = create_access_token(
        {'username': user.username, 'password': user.password})
    return {"user": user, "access_token": access_token}


def login_user(login_form: LoginForm):
    db_user = get_user(username=login_form.username)
    if not db_user:
        raise HTTPException(
            status_code=RECORD_NOT_FOUND,
            detail=ErrorMessage.user_not_found)
    if login_form.password != db_user.password:
        raise HTTPException(
            status_code=RECORD_NOT_FOUND,
            detail=ErrorMessage.password_mismatch
        )
    access_token = create_access_token(login_form.dict())
    return {'user': db_user, 'access_token': access_token}

