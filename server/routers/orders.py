from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from server.services import order_service
from server.schemas.order_schema import OrderCreate, OrderResponse
from server.database import get_db
from server.models import Order

router = APIRouter(prefix = "/orders", tags = ["Orders"])

@router.post("", response_model = OrderResponse, status_code = status.HTTP_201_CREATED)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    #Temp. simulation until Auth implementation
    mock_user=1

    created_order: Order = order_service.create_order(db = db, order_data = order_in, user_id = mock_user)

    return created_order