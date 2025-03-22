import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from crud import select_user
from db import get_session
from models import User
from utils import decode_access_token

bearer_scheme = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        session=Depends(get_session)
):
    try:
        token = credentials.credentials
        payload = decode_access_token(token)
        user = await select_user(user_id=payload["user_id"], session=session)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid User")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")


async def get_current_admin(
        user: User = Depends(get_current_user)
):
    if user:
        if user.is_admin:
            return user
        else:
            raise HTTPException(status_code=403, detail="Forbidden: need admin rights")
