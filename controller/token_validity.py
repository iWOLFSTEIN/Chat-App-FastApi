from functools import wraps
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import ALGORITHM
from secret import SECRET_KEY
from utils.error_message import ErrorMessage


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