from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from server.schemas.catalog_schema import ExportResult, CatalogItem, CatalogItemUpdate
from server.api.deps import RoleChecker
from server.constants import UserRole
from server.models import User
from server.database import get_db
from server.services import catalog_service

### --------------------------------------------------###

router = APIRouter(prefix = "/catalog", tags = ["Catalog"])
all_roles = RoleChecker([UserRole.ADMIN, UserRole.COMMERCIAL, UserRole.WAREHOUSE])
catalog_managers = RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE])

### --------------------------------------------------###

@router.post("/json/export", response_model = ExportResult, status_code = status.HTTP_200_OK)
def export_catalog_json(db: Session = Depends(get_db), current_user: User = Depends(catalog_managers)):
    return catalog_service.export_catalog_json(db = db)

@router.get("/json", response_model = list[CatalogItem], status_code = status.HTTP_200_OK)
def read_catalog_json(current_user: User = Depends(all_roles)):
    return catalog_service.read_catalog_json()

@router.put("/json/{sku}", response_model = CatalogItem, status_code = status.HTTP_200_OK)
def update_catalog_item_json(sku: str, item_in: CatalogItemUpdate, current_user: User = Depends(catalog_managers)):
    return catalog_service.update_catalog_item_json(sku = sku, changes = item_in.model_dump(exclude_none = True))

@router.delete("/json/{sku}", status_code = status.HTTP_204_NO_CONTENT)
def delete_catalog_item_json(sku: str, current_user: User = Depends(catalog_managers)):
    catalog_service.delete_catalog_item_json(sku = sku)

