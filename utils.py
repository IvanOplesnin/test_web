import datetime
import hashlib
import os

import jwt

from models import User


def hash_string(string):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


def equal_hash(hash_1: str, hash_2: str):
    return hash_string(hash_1) == hash_string(hash_2)


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
    import dotenv

    dotenv.load_dotenv()
    key = os.getenv("PAYMENT_KEY")
    string = f"{2}{1000}{"kldhashgdfaklaklj231321shd"}{3}{key}"
    hash_string = hash_string(string)
    dict_t = {
        "transaction_id": "kldhashgdfaklaklj231321shd",
        "user_id": 3,
        "account_id": 2,
        "amount": 1000,
        "signature": hash_string
    }
    print(dict_t)
