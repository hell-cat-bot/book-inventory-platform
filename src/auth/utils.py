import bcrypt
from datetime import timedelta, datetime
import jwt
import uuid
import logging

from src.books.config import Config

ACCESS_TOKEN_EXPIRY = 3600


def generate_passwd_hash(password: str) -> str:
    # Generate a salt and hash the password (encoding string to bytes)
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_passwd(password: str, hash: str) -> bool:
    # Verify the password by comparing bytes
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):

    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(
        uuid.uuid4()
    )  # since uuid.uuid4 is an UUID obj but we wanna convert it into a json serializable format
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )

    return token


# token decoding may fail due to expiry, signature verification
def decode_token(token: str) -> str | None:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=Config.JWT_ALGORITHM
        )

        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
