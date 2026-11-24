import os
import sys
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from server.core.config import RSA_KEYS_DIR, RSA_PRIVATE_KEY_FILE, RSA_PUBLIC_KEY_FILE

### --------------------------------------------------###

KEY_SIZE = 2048

def generate_keys() -> None:
    if RSA_PRIVATE_KEY_FILE.exists():
        print(f"[!] {RSA_PRIVATE_KEY_FILE} already exists. Delete it first if you really want new keys.")
        sys.exit(1)

    RSA_KEYS_DIR.mkdir(parents = True, exist_ok = True)

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

    RSA_PRIVATE_KEY_FILE.write_bytes(private_pem)
    RSA_PUBLIC_KEY_FILE.write_bytes(public_pem)
    os.chmod(RSA_PRIVATE_KEY_FILE, 0o600)

    print(f"[+] RSA-{KEY_SIZE} key pair created in {RSA_KEYS_DIR}/")

if __name__ == "__main__":
    generate_keys()