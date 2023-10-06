from functools import wraps
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import ALGORITHM
from controller import users
from models.user import User
from secret import SECRET_KEY
from utils.error_message import ErrorMessage
from utils.exceptions import http_exception_403


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def check_token_validity(func):
    @wraps(func)
    def decorator(**kwargs):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessage.invalid_token,
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(kwargs['token'], SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get('username')
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        kwargs.pop('token')
        return func(**kwargs)
    return decorator


def validate_user_for_signup(func):
    @wraps(func)
    def decorator(**kwargs):
        user: User = kwargs.get('user')
        db_user_by_username = users.get_user_by_query(
            query={'username': user.username})  
        if db_user_by_username:
            http_exception_403(detail=ErrorMessage.username_already_exist)
        db_user_by_email = users.get_user_by_query(query={'email': user.email})
        if db_user_by_email:
            http_exception_403(detail=ErrorMessage.email_already_exist)
        return func(**kwargs)
    return decorator