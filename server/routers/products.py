from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import Product
from server.services import product_service
from server.schemas.product_schema import ProductResponse

### --------------------------------------------------###

router = APIRouter(prefix = "/products", tags = ["Products"])

@router.get("", response_model = list[ProductResponse], status_code = status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    products: list[Product] = product_service.get_all_products(db)
    return products
    