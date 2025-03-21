import hashlib


def hash_password(password):
    return hashlib.sha256(bytes(password, 'utf-8')).hexdigest()


def equal_hash(hash_1: str, hash_2: str):
    return hash_password(hash_1) == hash_password(hash_2)
