from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from crud import select_user_by_email
from db import get_session
from models import User
from schemas import AuthRead
from utils import hash_string, create_access_token

login_router = APIRouter(prefix="/login")


@login_router.post("/")
async def login_post(auth: AuthRead, session=Depends(get_session)):
    user: User = await select_user_by_email(email=auth.email, session=session)
    if user:
        if hash_string(auth.password) == user.hash_password:
            access_token = create_access_token(user)
            return {
                "access_token": access_token,
                "type": "bearer"
            }
    raise HTTPException(status_code=401, detail="Invalid username or password")
