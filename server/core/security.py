import secrets
import hashlib

from .config import PEPPER

### --------------------------------------------------###

def generate_salt() -> str:
    return secrets.token_hex(16)

def generate_hashed_password(plain_password: str, salt: str) -> str:
    chain = plain_password + salt + PEPPER
    return hashlib.sha256(chain.encode("utf-8")).hexdigest()

def verify_password(plain_password: str, salt: str, hashed_password: str) -> bool:
    calculated_hash: str = generate_hashed_password(plain_password = plain_password, salt = salt)
    return secrets.compare_digest(calculated_hash, hashed_password)

