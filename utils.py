import datetime
import hashlib
import os
import time

import jwt

from models import User


def hash_password(password):
    return hashlib.sha256(bytes(password, 'utf-8')).hexdigest()


def equal_hash(hash_1: str, hash_2: str):
    return hash_password(hash_1) == hash_password(hash_2)


def create_access_token(user: User):
    secret = os.getenv("SECRET_KEY")
    print(secret)
    encode = jwt.encode(
        {
            "user_id": user.id,
            "is_admin": user.is_admin,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
        },
        secret,
        algorithm="HS256"
    )
    return encode


def decode_access_token(token):
    secret = os.getenv("SECRET_KEY")
    try:
        decode = jwt.decode(
            token,
            secret,
            algorithms=["HS256"]
        )
        return decode
    except jwt.exceptions.InvalidSignatureError as e:
        raise jwt.exceptions.InvalidSignatureError('Invalid key')
    except jwt.exceptions.ExpiredSignatureError as e:
        raise jwt.exceptions.ExpiredSignatureError('Expired token')
    except jwt.exceptions.InvalidTokenError as e:
        raise jwt.exceptions.InvalidTokenError('Invalid token')


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    token = create_access_token(User(id=1, is_admin=True, email="test@test.com", hash_password='1231', fullname='test'))
    print(token)
    decode = decode_access_token(token)
    print(decode)
    time.sleep(31)
    decode = decode_access_token(token)
    print(decode)
