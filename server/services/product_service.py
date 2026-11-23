from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends, HTTPException, status

from server.models import Product
from server.schemas.product_schema import ProductCreate, ProductUpdate
from server.database import get_db

### --------------------------------------------------###

def get_product_by_id(product_id: int, db: Session) -> Product | None:
    stmt = select(Product).where(Product.id == product_id)
    return db.execute(stmt).scalar_one_or_none()

### --------------------------------------------------###

def get_all_products(order_by: str, sort_order: str, category: str | None, db: Session) -> list[Product]:

    allowed_columns : list[str] = ["id", "name", "base_price", "stock"]
    if order_by not in allowed_columns:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid column for order"
        )

    sort_column = getattr(Product, order_by)
    if sort_order.lower() == "desc":
        sort_criteria = sort_column.desc()
    
    else:
        sort_criteria = sort_column.asc()

    stmt = select(Product)
    if category is not None:
        stmt = stmt.where(Product.category == category)
        
    stmt = stmt.order_by(sort_criteria)
    return list(db.scalars(stmt).all())

def create_product(product_in: ProductCreate, db: Session) -> Product:
    try:
        stmt = select(Product).where(Product.sku == product_in.sku)
        product = db.execute(stmt).scalar_one_or_none()

        if product:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = f"Product with sku {product_in.sku} already exists"
            )
        
        new_product: Product = Product(
            sku = product_in.sku,
            name = product_in.name,
            description = product_in.description,
            category = product_in.category,
            base_price = product_in.base_price,
            stock = product_in.stock
            )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Something went wrong while creating product"
        )

def insert_image(product_id: int, image: bytes, content_type: str | None, db: Session) -> Product:
    if not content_type or not content_type.startswith("image/"):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "File format not supported"
        )
    
    try:
        product = get_product_by_id(product_id = product_id, db = db)
        if not product:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Product with ID {product_id} not found"
            )
        product.image = image

        db.commit()
        db.refresh(product)
        return product

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        print(repr(e))
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An error occurred"
        )

def get_product_image(product_id: int, db: Session) -> bytes:
    try:
        product = get_product_by_id(product_id = product_id, db = db)
        if not product:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Product with ID {product_id} not found"
            )
        if not product.image:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Product with ID {product_id} has no image"
            )
        return product.image

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An error occurred"
        )

def update_product(product_id: int, product_in: ProductUpdate, db: Session) -> Product:
    try:
        product = get_product_by_id(product_id = product_id, db = db)
        if not product:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Product with product ID {product_id} not found"
            )
        changes = product_in.model_dump(exclude_none = True)

        if "sku" in changes and changes["sku"] != product.sku:
            stmt = select(Product).where(Product.sku == changes["sku"])
            if db.execute(stmt).scalar_one_or_none():
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = f"Product with sku {changes['sku']} already exists"
                )

        for field, value in changes.items():
            setattr(product, field, value)

        db.commit()
        db.refresh(product)
        return product

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An error occurred"
        ) from e

def delete_product(product_id: int, db: Session) -> None:
    try:
        product = get_product_by_id(product_id = product_id, db = db)
        if not product:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Product with product ID {product_id} not found"
            )
        
        if product.order_items:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"Product with ID {product_id} cannot be deleted because it appears in existing orders"
            )

        db.delete(product)
        db.commit()

    except HTTPException:
        db.rollback()
        raise
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An error occurred"
        ) from e
