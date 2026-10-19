from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import Product, User
from server.services import product_service
from server.schemas.product_schema import ProductResponse
from server.api.deps import RoleChecker
from server.constants import UserRole

### --------------------------------------------------###

router = APIRouter(prefix = "/products", tags = ["Products"])

@router.get("", response_model = list[ProductResponse], status_code = status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    products: list[Product] = product_service.get_all_products(db)
    return products

@router.post("", response_model = ProductResponse, status_code = status.HTTP_201_CREATED)
def create_product(current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE]))):
    pass

@router.delete("", response_model = ProductResponse, status_code = status.HTTP_200_OK)
def delete_product(current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE]))):
    pass

@router.put("", response_model = ProductResponse, status_code = status.HTTP_200_OK)
def update_product(current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE]))):
    pass
    