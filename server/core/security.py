import secrets
import hashlib
import jwt
from datetime import datetime, timezone, timedelta

from .config import PEPPER, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from server.schemas.auth_schema import Token, TokenData

### --------------------------------------------------###

def generate_salt() -> str:
    return secrets.token_hex(16)

def generate_hashed_password(plain_password: str, salt: str) -> str:
    chain = plain_password + salt + PEPPER
    return hashlib.sha256(chain.encode("utf-8")).hexdigest()

def verify_password(plain_password: str, salt: str, hashed_password: str) -> bool:
    calculated_hash: str = generate_hashed_password(plain_password = plain_password, salt = salt)
    return secrets.compare_digest(calculated_hash, hashed_password)

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