from typing import Annotated
from fastapi import APIRouter, Depends, Query
from controller.users import get_users
from controller.token_validity import oauth2_scheme

router = APIRouter()

@router.get('/users')
async def users(
    token: Annotated[str, Depends(oauth2_scheme)], 
    limit: Annotated[int, Query()] = 20
    ):
    return get_users(max_limit=limit, token=token)