from datetime import datetime, timedelta
from fastapi import HTTPException, status
from controller.users import get_user_by_id, get_user_by_query
from controller.validate import validate_user_for_signup
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
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@validate_user_for_signup
def create_user(user: User):
    db = MongoStore.mongo_db()
    new_user = user.dict(exclude={'id'})
    result = db[MongoCollections.users].insert_one(new_user)
    access_token = create_access_token(
        {'username': user.username, 'password': user.password})
    
    user_id = result.inserted_id.__str__()
    user = get_user_by_id(token=access_token, id=user_id)
    
    return {"user": user, "access_token": access_token}


def login_user(login_form: LoginForm):
    user = get_user_by_query(
        query=login_form.dict(exclude={'password'}, exclude_none=True, by_alias=True))
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

