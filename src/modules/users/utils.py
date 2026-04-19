from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.core.config import settings

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth.JWT_PRIVATE,
    algorithm: str = settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(
        to_encode,
        key=private_key,
        algorithm=algorithm
    )
    return encoded

def decode_jwt(
    token: str,
    public_key: str = settings.auth.JWT_PUBLIC,
    algorithm: str = settings.auth.algorithm
) -> dict:
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm]
    )
    return decoded


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    encoded: bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return encoded.decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8")
    )
