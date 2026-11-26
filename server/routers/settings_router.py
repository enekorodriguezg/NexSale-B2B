from fastapi import APIRouter, status, Depends

from server.schemas.settings_schema import SettingsResponse, SettingsUpdate
from server.services import settings_service
from server.models import User
from server.api.deps import RoleChecker
from server.constants import UserRole

### --------------------------------------------------###

router = APIRouter(prefix = "/settings", tags = ["Settings"])

@router.get("", response_model = SettingsResponse, status_code = status.HTTP_200_OK)
def get_settings(current_user: User = Depends(RoleChecker([UserRole.ADMIN]))) -> SettingsResponse:
    return settings_service.get_settings()

@router.put("", response_model = SettingsResponse, status_code = status.HTTP_200_OK)
def update_settings(settings_in: SettingsUpdate, current_user: User = Depends(RoleChecker([UserRole.ADMIN]))) -> SettingsResponse:
    return settings_service.update_settings(settings_in = settings_in)

