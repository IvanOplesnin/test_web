from fastapi import APIRouter
from fastapi.params import Depends

from models import User
from schemas import UserRead, AccountRead, TransactionRead
from security import get_current_user

user_router = APIRouter(prefix='/users')


@user_router.get("/info", response_model=UserRead)
async def get_user_info(user: User = Depends(get_current_user)):
    return user


@user_router.get("/accounts", response_model=list[AccountRead])
async def get_user_accounts(user: User = Depends(get_current_user)):
    accounts = user.accounts
    return accounts


@user_router.get("/transactions", response_model=list[TransactionRead])
async def get_user_transactions(user: User = Depends(get_current_user)):
    transactions = user.transactions
    return transactions
