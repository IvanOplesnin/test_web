from fastapi import APIRouter, Depends

from crud import get_all_users, user_add, user_update, user_delete
from db import get_session
from schemas import UserReadWithAccounts, UserCreate, UserUpdate, UserRead
from security import get_current_admin

admin_routes = APIRouter(
    prefix='/admin',
    dependencies=[Depends(get_current_admin)]
)


@admin_routes.get('/all_users', response_model=list[UserReadWithAccounts])
async def all_users(session=Depends(get_session)):
    users = await get_all_users(session=session)
    return users


@admin_routes.post("/create_user", response_model=UserRead)
async def create_user(user: UserCreate, session=Depends(get_session)):
    new_user = await user_add(user=user, session=session)
    return new_user


@admin_routes.patch("/update_user/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, session=Depends(get_session)):
    updating_user = await user_update(user_id=user_id, user=user, session=session)
    return updating_user


@admin_routes.delete("/delete_user/{user_id}")
async def delete_user(user_id: int, session=Depends(get_session)):
    await user_delete(user_id=user_id, session=session)

