from fastapi import APIRouter, status, Depends, UploadFile, Response
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import Product, User
from server.services import product_service
from server.schemas.product_schema import ProductCreate, ProductResponse
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

@router.delete("/{product_id}", status_code = status.HTTP_204_NO_CONTENT) #TODO
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE]))):
    pass

@router.put("/{product_id}", status_code = status.HTTP_200_OK) #TODO
def update_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE]))):
    pass

@router.put("/{product_id}/image", status_code = status.HTTP_200_OK)
async def insert_image(product_id: int, image: bytes, file: UploadFile, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE]))):
    image_bytes = await file.read()
    content_type = file.content_type
    product = product_service.insert_image(product_id = product_id, image = image_bytes, content_type = content_type, db = db)
    return product

@router.get("/{product_id}/image", status_code = status.HTTP_200_OK)
def get_product_image(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.COMMERCIAL, UserRole.WAREHOUSE]))):
    image_bytes = product_service.get_product_image(product_id = product_id, db = db)
    return Response(content = image_bytes, media_type = "image/jpeg")

    