import binascii

from fastapi import HTTPException, status

from server.schemas.security_schema import PublicKeyResponse, EncryptedMessage, DecryptedMessage
from server.core import rsa_crypto

### --------------------------------------------------###

def get_public_key() -> PublicKeyResponse:
    return PublicKeyResponse(public_key_pem = rsa_crypto.get_public_key_pem())

def decrypt_message(message: EncryptedMessage) -> DecryptedMessage:
    try:
        plain_text = rsa_crypto.rsa_decrypt(token = message.ciphertext)
    except (ValueError, binascii.Error) as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Message could not be decrypted with the server private key"
        ) from e
    
    return DecryptedMessage(plain_text = plain_text)
