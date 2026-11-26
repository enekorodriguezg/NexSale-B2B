import json
import threading

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from server.models import Product
from server.core.config import CATALOG_JSON_FILE

### --------------------------------------------------###

_json_lock = threading.Lock()

### --------------------------------------------------###

def _load_json() -> list[dict]:
    if not CATALOG_JSON_FILE.exists():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Catalog has not been exported to JSON yet"
        )
    with open(CATALOG_JSON_FILE, "r", encoding = "utf-8") as file:
        return json.load(file)

def _save_json(catalog: list[dict]) -> None:
    CATALOG_JSON_FILE.parent.mkdir(parents = True, exist_ok = True)
    with open(CATALOG_JSON_FILE, "w", encoding = "utf-8") as file:
        json.dump(catalog, file, indent = 2, ensure_ascii = False)

def _find_index(catalog: list[dict], sku: str) -> int:
    for index, item in enumerate(catalog):
        if item["sku"] == sku:
            return index

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"Product with sku {sku} not found in the catalog file"
    )

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

def export_catalog_json(db: Session) -> int:
    products = db.scalars(select(Product).order_by(Product.sku)).all()
    catalog = [_product_to_dict(product) for product in products]

    with _json_lock:
        _save_json(catalog)

    return len(catalog)

def read_catalog_json() -> list[dict]:
    with _json_lock:
        return _load_json()

def update_catalog_item_json(sku: str, changes: dict) -> dict:
    with _json_lock:
        catalog = _load_json()
        index = _find_index(catalog = catalog, sku = sku)
        catalog[index].update(changes)
        _save_json(catalog = catalog)
        return catalog[index]

def delete_catalog_item_json(sku: str) -> None:
    with _json_lock:
        catalog = _load_json()
        index = _find_index(catalog = catalog, sku = sku)
        catalog.pop(index)
        _save_json(catalog = catalog)