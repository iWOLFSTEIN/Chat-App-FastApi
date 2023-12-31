from typing import Annotated
from fastapi import APIRouter, Depends, Query
from controller.users import get_user_by_id, get_users
from controller.validate import oauth2_scheme
from utils.error_message import ErrorMessage

router = APIRouter()


@router.get("/users")
async def users(
    token: Annotated[str, Depends(oauth2_scheme)], limit: Annotated[int, Query()] = 20
):
    return get_users(max_limit=limit, token=token)


@router.get("/user")
async def single_user(
    token: Annotated[str, Depends(oauth2_scheme)], id: Annotated[str, Query()]
):
    user = get_user_by_id(id=id, token=token)
    if user:
        return user
    return {"message": ErrorMessage.user_not_found}
