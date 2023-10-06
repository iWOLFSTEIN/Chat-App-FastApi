from datetime import datetime, timedelta
from controller.users import get_user_by_id
from controller.validate import validate_user_for_signup, validate_user_for_login
from models.login_form import LoginForm
from models.user import User
from secret import SECRET_KEY 
from config import ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS
from jose import jwt
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


@validate_user_for_login
def login_user(login_form: LoginForm, user: User):   
    access_token = create_access_token(
        {'username': user.username, 'password': user.password})
    return {'user': user, 'access_token': access_token}

