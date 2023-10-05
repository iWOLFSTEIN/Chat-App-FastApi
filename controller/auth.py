from datetime import datetime, timedelta
from fastapi import HTTPException, status
from controller.users import get_single_user
from models.login_form import LoginForm
from models.user import User
from secret import SECRET_KEY 
from config import ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS
from jose import jwt
from utils.error_message import ErrorMessage
from controller.mongo_db import MongoCollections, MongoStore


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        # expire = datetime.utcnow() + timedelta(seconds=5)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(username: str) -> User | None:
    db = MongoStore().mongo_db()
    query = {'username': username}
    user = db[MongoCollections.users].find_one(query)
    if user:
        return User(**user)
    return None 


def create_user(user: User):
    db = MongoStore().mongo_db()
    db_user = get_user(username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorMessage.user_already_exist)
    result = db[MongoCollections.users].insert_one(user.dict())
    access_token = create_access_token(
        {'username': user.username, 'password': user.password})
    user = get_single_user(token=access_token, id=result.inserted_id)
    return {"user": user, "access_token": access_token}


def login_user(login_form: LoginForm):
    user = get_user(username=login_form.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.user_not_found)
    if login_form.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.password_mismatch
        )
    access_token = create_access_token(
        {'username': user.username, 'password': user.password})
    return {'user': user, 'access_token': access_token}

