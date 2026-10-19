from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from server.services import order_service
from server.schemas.order_schema import OrderCreate, OrderResponse
from server.database import get_db
from server.models import Order, User
from server.constants import UserRole
from server.api.deps import RoleChecker

### --------------------------------------------------###

router = APIRouter(prefix = "/orders", tags = ["Orders"])

@router.post("", response_model = OrderResponse, status_code = status.HTTP_201_CREATED)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMMERCIAL, UserRole.ADMIN]))):
    created_order: Order = order_service.create_order(db = db, order_data = order_in, user_id = current_user.id) #type: ignore
    return created_order

@router.get("", response_model = list[OrderResponse], status_code = status.HTTP_200_OK)
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.COMMERCIAL, UserRole.WAREHOUSE]))) -> list[Order]:
    orders: list[Order] = order_service.get_orders(db = db, current_user = current_user)
    return orders
    

@router.delete("")
def delete_order():
    pass

@router.put("")
def update_order():
    pass