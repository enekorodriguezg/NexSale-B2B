import os
import sys
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

### --------------------------------------------------###

KEYS_DIR = Path(os.getenv("RSA_KEYS_DIR", "keys"))
PRIVATE_KEY_FILE = KEYS_DIR / "private_key.pem"
PUBLIC_KEY_FILE = KEYS_DIR / "public_key.pem"
KEY_SIZE = 2048

def generate_keys() -> None:
    if PRIVATE_KEY_FILE.exists():
        print(f"[!] {PRIVATE_KEY_FILE} already exists. Delete it first if you really want new keys.")
        sys.exit(1)

    KEYS_DIR.mkdir(parents = True, exist_ok = True)

    private_key = rsa.generate_private_key(public_exponent = 65537, key_size = KEY_SIZE)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.PKCS8,
        encryption_algorithm = serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PublicFormat.SubjectPublicKeyInfo
    )

    PRIVATE_KEY_FILE.write_bytes(private_pem)
    PUBLIC_KEY_FILE.write_bytes(public_pem)
    os.chmod(PRIVATE_KEY_FILE, 0o600)

    print(f"[+] RSA-{KEY_SIZE} key pair created in {KEYS_DIR}/")

if __name__ == "__main__":
    generate_keys()