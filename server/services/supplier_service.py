import json
import threading

from fastapi import HTTPException, status

from server.core.config import SUPPLIERS_JSON_FILE

### --------------------------------------------------###

_json_lock = threading.Lock()

### --------------------------------------------------###

def _load_json() -> list[dict]:
    if not SUPPLIERS_JSON_FILE.exists():
        return []
    with open(SUPPLIERS_JSON_FILE, "r", encoding = "utf-8") as file:
        return json.load(file)

def _save_json(suppliers: list[dict]) -> None:
    SUPPLIERS_JSON_FILE.parent.mkdir(parents = True, exist_ok = True)
    with open(SUPPLIERS_JSON_FILE, "w", encoding = "utf-8") as file:
        json.dump(suppliers, file, indent = 2, ensure_ascii = False)

def _find_index(suppliers: list[dict], code: str) -> int:
    for index, supplier in enumerate(suppliers):
        if supplier["code"] == code:
            return index

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"Supplier with code {code} not found"
    )

### --------------------------------------------------###

def get_suppliers(category: str | None = None) -> list[dict]:
    with _json_lock:
        suppliers = _load_json()
        if category is not None:
            suppliers = [supplier for supplier in suppliers if supplier["category"] == category]
        return suppliers

def create_supplier(supplier: dict) -> dict:
    with _json_lock:
        suppliers = _load_json()
        if any(existing["code"] == supplier["code"] for existing in suppliers):
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"Supplier with code {supplier['code']} already exists"
            )
        suppliers.append(supplier)
        _save_json(suppliers = suppliers)
        return supplier

def update_supplier(code: str, changes: dict) -> dict:
    with _json_lock:
        suppliers = _load_json()
        index = _find_index(suppliers = suppliers, code = code)
        suppliers[index].update(changes)
        _save_json(suppliers = suppliers)
        return suppliers[index]

def delete_supplier(code: str) -> None:
    with _json_lock:
        suppliers = _load_json()
        index = _find_index(suppliers = suppliers, code = code)
        suppliers.pop(index)
        _save_json(suppliers = suppliers)