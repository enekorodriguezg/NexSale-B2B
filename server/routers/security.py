from fastapi import APIRouter, status, Depends

from server.schemas.security_schema import PublicKeyResponse, DecryptedMessage, EncryptedMessage
from server.services import security_service
from server.models import User
from api.deps import RoleChecker
from server.constants import UserRole

### --------------------------------------------------###

router = APIRouter(prefix = "/security", tags = ["Security"])

@router.get("/public_key", response_model = PublicKeyResponse, status_code = status.HTTP_200_OK)
def get_public_key() -> PublicKeyResponse:
    return security_service.get_public_key()

@router.post("/decrypt", response_model = DecryptedMessage, status_code = status.HTTP_200_OK)
def decrypt_message(message: EncryptedMessage, current_user: User = Depends(RoleChecker([UserRole.ADMIN]))) -> DecryptedMessage:
    return security_service.decrypt_message(message = message)
