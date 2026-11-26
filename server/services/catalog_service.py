import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from server.models import Product
from server.core.config import CATALOG_JSON_FILE

### --------------------------------------------------###

def _product_to_dict(product: Product) -> dict:
    return {
        "sku": product.sku,
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "base_price": product.base_price,
        "stock": product.stock,
    }

def export_catalog(db: Session) -> int:
    products = db.scalars(select(Product).order_by(Product.sku)).all()
    catalog = [_product_to_dict(product) for product in products]

    CATALOG_JSON_FILE.parent.mkdir(parents = True, exist_ok = True)
    with open(CATALOG_JSON_FILE, "w", encoding = "utf-8") as file:
        json.dump(catalog, file, indent = 2, ensure_ascii = False)

    return len(catalog)