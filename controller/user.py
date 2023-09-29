from datetime import datetime, timedelta
from fastapi import HTTPException
from models.login_form import LoginForm
from models.user import User
from secret import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS
from jose import jwt
from utils.error_message import ErrorMessage
from utils.status_codes import ALREADY_EXIST, RECORD_NOT_FOUND

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

def create_user(user: User):
    db_user = dummy_user_db.get(user.username)
    if db_user:
        raise HTTPException(
            status_code=ALREADY_EXIST,
            detail=ErrorMessage.user_already_exist)
    dummy_user_db.update({user.username: user})
    access_token = create_access_token(
        {'username': user.username, 'password': user.password})
    return {"user": user, "access_token": access_token}


def login_user(login_form: LoginForm):
    db_user = dummy_user_db.get(login_form.username)
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

