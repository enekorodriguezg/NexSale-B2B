from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import Product, User
from server.services import product_service
from server.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from server.api.deps import RoleChecker
from server.constants import UserRole

### --------------------------------------------------###

router = APIRouter(prefix = "/products", tags = ["Products"])

@router.get("", response_model = list[ProductResponse], status_code = status.HTTP_200_OK)
def get_products(order_by: str = "id", sort_order: str = "asc", db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.COMMERCIAL, UserRole.WAREHOUSE]))):
    products: list[Product] = product_service.get_all_products(order_by = order_by, sort_order = sort_order, db = db)
    return products

@router.post("", response_model = ProductResponse, status_code = status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE]))):
    created_product = product_service.create_product(product_in = product_in, db = db)
    return created_product

@router.delete("/{product_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE]))):
    pass

@router.put("/{product_id}", response_model = ProductUpdate, status_code = status.HTTP_200_OK)
def update_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE]))):
    pass
    