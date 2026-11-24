"""R24 demo client: encrypts a message with the NexSale public key (RSA-OAEP)
and sends it to the server, which is the only one able to decrypt it.

Usage (from inside the API container, talking to Apache):
    docker compose exec -e NEXSALE_URL=http://apache nexsale_api python scripts/send_secure_message.py "HR1210010051863000160"
"""

import os
import sys
import json
import base64
import urllib.parse
import urllib.request

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

### --------------------------------------------------###

BASE_URL = os.getenv("NEXSALE_URL", "http://localhost")
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin"


def get_json(url: str, data: bytes | None = None, headers: dict | None = None) -> dict:
    request = urllib.request.Request(url, data = data, headers = headers or {})
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def main(message: str) -> None:
    #1. Download the server public key (anyone can do this)
    public_pem = get_json(f"{BASE_URL}/security/public-key")["public_key_pem"]
    public_key = serialization.load_pem_public_key(public_pem.encode("ascii"))
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise ValueError("The server public key is not an RSA key")
    print("[1] Public key downloaded")

    #2. Encrypt locally with the public key
    ciphertext = public_key.encrypt(
        message.encode("utf-8"),
        padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None)
    )
    ciphertext_b64 = base64.b64encode(ciphertext).decode("ascii")
    print(f"[2] Encrypted message (what travels over the network):\n    {ciphertext_b64[:60]}...")

    #3. Send it to the server, which decrypts it with its private key
    login_data = urllib.parse.urlencode({"username": ADMIN_USER, "password": ADMIN_PASSWORD}).encode()
    token = get_json(f"{BASE_URL}/auth/login", data = login_data)["access_token"]
    result = get_json(
        f"{BASE_URL}/security/decrypt",
        data = json.dumps({"ciphertext": ciphertext_b64}).encode(),
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    print(f"[3] Server decrypted it as: {result['plain_text']}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "HR1210010051863000160")