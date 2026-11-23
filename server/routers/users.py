from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from server.schemas.user_schema import UserResponse
from server.models import User
from server.database import get_db
from server.api.deps import RoleChecker
from server.constants import UserRole
from server.services import user_service

### --------------------------------------------------###

router = APIRouter(prefix = "/users", tags = ["Products"])

@router.get("", response_model = list[UserResponse], status_code = status.HTTP_200_OK)
def get_all_users(order_by: str = "id", sort_order: str = "asc", db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN]))):
    users: list[User] = user_service.get_all_users(order_by = order_by, sort_order = sort_order, db = db)
    return users