import os
import base64

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

from .config import AES_KEY

### --------------------------------------------------###

NONCE_SIZE = 12
_aesgcm = AESGCM(AES_KEY)

def encrypt_text(plain_text: str) -> str:
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = _aesgcm.encrypt(nonce, plain_text.encode("utf-8"), None)
    return base64.b64encode(nonce + ciphertext).decode("ascii")

def decrypt_text(token: str) -> str:
    data = base64.b64decode(token)
    nonce = data[:NONCE_SIZE]
    ciphertext = data[NONCE_SIZE:]

    try:
        plain_bytes = _aesgcm.decrypt(nonce, ciphertext, None)

    except InvalidTag as e:
        raise ValueError("Encrypted data was tampered with or the key is wrong") from e

    return plain_bytes.decode("utf-8")
