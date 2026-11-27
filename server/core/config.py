import os
from dotenv import load_dotenv
import base64
import binascii
from pathlib import Path

### --------------------------------------------------###

load_dotenv()

SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback_jwt_inseguro")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8 #8 hours sessions

_aes_key_b64 = os.getenv("AES_KEY")
if not _aes_key_b64:
    raise RuntimeError("AES_KEY is not set in the environment")

try:
    AES_KEY: bytes = base64.b64decode(_aes_key_b64, validate = True)
except binascii.Error as e:
    raise RuntimeError("AES_KEY is not valid Base64") from e

if len(AES_KEY) != 32:
    raise RuntimeError(f"AES_KEY must be 32 bytes (AES-256), got {len(AES_KEY)}")

RSA_KEYS_DIR: Path = Path(os.getenv("RSA_KEYS_DIR", "keys"))
RSA_PRIVATE_KEY_FILE: Path = RSA_KEYS_DIR / "private_key.pem"
RSA_PUBLIC_KEY_FILE: Path = RSA_KEYS_DIR / "public_key.pem"

DATA_DIR: Path = Path(os.getenv("DATA_DIR", "data"))
CATALOG_JSON_FILE: Path = DATA_DIR / "catalog.json"