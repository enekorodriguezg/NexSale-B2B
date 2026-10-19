from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends, HTTPException, status

from server.models import Product
from server.schemas.product_schema import ProductCreate, ProductResponse
from server.database import get_db

### --------------------------------------------------###

def get_all_products(db: Session) -> list[Product]:
    stmt = select(Product)
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
        print(f"\n--- ERROR REAL QUE ESTOY OCULTANDO: {repr(e)} ---\n")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Something went wrong while creating product"
        )


    