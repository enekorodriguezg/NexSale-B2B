from fastapi import APIRouter, status, Depends

from server.models import User
from server.api.deps import RoleChecker
from server.constants import UserRole
from server.services import backup_service
from server.schemas.backup_schema import BackupResult

### --------------------------------------------------###

router = APIRouter(prefix = "/backups", tags = ["Backups"])

### --------------------------------------------------###

@router.post("", response_model = BackupResult, status_code = status.HTTP_201_CREATED)
def create_backup(current_user: User = Depends(RoleChecker([UserRole.ADMIN]))):
    return backup_service.create_backup()  