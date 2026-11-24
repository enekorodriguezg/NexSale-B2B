from pydantic import BaseModel, Field

### --------------------------------------------------###

class PublicKeyResponse(BaseModel):
    public_key_pem: str


class EncryptedMessage(BaseModel):
    ciphertext: str = Field(min_length = 1)

class DecryptedMessage(BaseModel):
    plain_text: str
