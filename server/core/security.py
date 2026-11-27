import secrets
import hashlib
import jwt
from datetime import datetime, timezone, timedelta
import string

from .config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from server.schemas.auth_schema import Token, TokenData

### --------------------------------------------------###

PEPPER_ALPHABET = string.ascii_letters

### --------------------------------------------------###

def generate_salt(user_id: int) -> str:
    return hashlib.sha256(f"nexsale-user-{user_id}".encode("utf-8")).hexdigest()

def _hash_password(plain_password: str, salt: str, pepper: str) -> str:
    return hashlib.sha256((plain_password + salt + pepper).encode("utf-8")).hexdigest()

def generate_hashed_password(plain_password: str, user_id: int) -> str:
    salt = generate_salt(user_id = user_id)
    pepper = secrets.choice(PEPPER_ALPHABET)
    return _hash_password(plain_password = plain_password, salt = salt, pepper = pepper)

def verify_password(plain_password: str, user_id: int, hashed_password: str) -> bool:
    salt = generate_salt(user_id = user_id)
    is_valid = False
    for pepper in PEPPER_ALPHABET:
        if secrets.compare_digest(_hash_password(plain_password = plain_password, salt = salt, pepper = pepper), hashed_password):
            is_valid = True
    return is_valid

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode["exp"] = expire
    to_encode["iat"] = now

    access_token: str = jwt.encode(payload = to_encode, key = SECRET_KEY, algorithm = ALGORITHM)

    return access_token