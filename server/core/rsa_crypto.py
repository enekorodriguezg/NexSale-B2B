from functools import lru_cache
import base64

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

from server.core.config import RSA_PRIVATE_KEY_FILE

### --------------------------------------------------###

_OAEP = padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None)
_PSS = padding.PSS(mgf = padding.MGF1(hashes.SHA256()), salt_length = padding.PSS.MAX_LENGTH)

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

def get_public_key_pem() -> str:
     public_key = _get_private_key().public_key()
     return public_key.public_bytes(
          encoding = serialization.Encoding.PEM,
          format = serialization.PublicFormat.SubjectPublicKeyInfo
     ).decode("ascii")

def sign_data(data: bytes) -> str:
     signature = _get_private_key().sign(data, _PSS, hashes.SHA256())
     return base64.b64encode(signature).decode("ascii")

def verify_signature(data: bytes, signature_b64: str) -> bool:
     try:
          public_key = _get_private_key().public_key()
          public_key.verify(base64.b64decode(signature_b64), data, _PSS, hashes.SHA256())
          return True
     except (InvalidSignature, ValueError):
          return False

