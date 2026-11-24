from functools import lru_cache
import base64

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

from server.core.config import RSA_PRIVATE_KEY_FILE

### --------------------------------------------------###

_OAEP = padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None)

@lru_cache(maxsize = 1)
def _get_private_key() -> rsa.RSAPrivateKey:
    if not RSA_PRIVATE_KEY_FILE.exists():
         raise RuntimeError(f"RSA private key not found at {RSA_PRIVATE_KEY_FILE}. Run scripts/generate_rsa_keys.py")

    private_key = serialization.load_pem_private_key(RSA_PRIVATE_KEY_FILE.read_bytes(), password = None)
    
    if not isinstance(private_key, rsa.RSAPrivateKey):
         raise RuntimeError(f"{RSA_PRIVATE_KEY_FILE} is not an RSA private key")

    return private_key

def rsa_encrypt(plain_text: str) -> str:
     public_key = _get_private_key().public_key()
     ciphertext = public_key.encrypt(plain_text.encode("utf-8"), _OAEP)
     return base64.b64encode(ciphertext).decode("ascii")

def rsa_decrypt(token: str) -> str:
     plain_bytes = _get_private_key().decrypt(base64.b64decode(token), _OAEP)
     return plain_bytes.decode("utf-8")

