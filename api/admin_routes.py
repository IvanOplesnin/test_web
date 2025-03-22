from fastapi import APIRouter, Depends

from crud import get_all_users
from db import get_session
from models import User
from schemas import UserRead, UserReadWithAccounts
from security import get_current_admin

admin_routes = APIRouter(
    prefix='/admin',
    dependencies=[Depends(get_current_admin)]
)


@admin_routes.get('/all_users', response_model=list[UserReadWithAccounts])
async def all_users(session=Depends(get_session)):
    users = await get_all_users(session=session)
    return users
