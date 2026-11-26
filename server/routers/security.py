from fastapi import APIRouter, status, Depends, UploadFile, File, Form

from server.schemas.security_schema import PublicKeyResponse, DecryptedMessage, EncryptedMessage, SignatureVerification
from server.services import security_service
from server.models import User
from server.api.deps import RoleChecker, get_current_user
from server.constants import UserRole

### --------------------------------------------------###

router = APIRouter(prefix = "/security", tags = ["Security"])

@router.get("/public-key", response_model = PublicKeyResponse, status_code = status.HTTP_200_OK)
def get_public_key() -> PublicKeyResponse:
    return security_service.get_public_key()

@router.post("/decrypt", response_model = DecryptedMessage, status_code = status.HTTP_200_OK)
def decrypt_message(message: EncryptedMessage, current_user: User = Depends(RoleChecker([UserRole.ADMIN]))) -> DecryptedMessage:
    return security_service.decrypt_message(message = message)

@router.post("/verify", response_model = SignatureVerification, status_code = status.HTTP_200_OK)
async def verify_document(file: UploadFile = File(...), signature: str = Form(...), current_user: User = Depends(get_current_user)):
    document = await file.read()
    return security_service.verify_document(document = document, signature = signature)
