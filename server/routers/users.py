from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from server.schemas.user_schema import UserResponse, UserCreate, UserUpdate
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

@router.post("", response_model = UserResponse, status_code = status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN]))):
    user = user_service.create_user(user_in = user_in, db = db)
    return user

@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN]))):
    user_service.delete_user(user_id = user_id, db = db, current_user = current_user)

@router.put("/{user_id}", response_model = UserResponse, status_code = status.HTTP_200_OK)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN]))):
    user = user_service.update_user(user_id = user_id, user_in = user_in, db = db, current_user = current_user)
    return user 