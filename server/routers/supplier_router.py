from fastapi import APIRouter, status, Depends

from server.schemas.supplier_schema import SupplierCreate, SupplierUpdate, SupplierResponse
from server.api.deps import RoleChecker
from server.constants import UserRole
from server.models import User
from server.services import supplier_service

### --------------------------------------------------###

router = APIRouter(prefix = "/suppliers", tags = ["Suppliers"])
supplier_managers = RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE])

### --------------------------------------------------###

@router.get("", response_model = list[SupplierResponse], status_code = status.HTTP_200_OK)
def get_suppliers(category: str | None = None, current_user: User = Depends(supplier_managers)):
    return supplier_service.get_suppliers(category = category)

@router.post("", response_model = SupplierResponse, status_code = status.HTTP_201_CREATED)
def create_supplier(supplier_in: SupplierCreate, current_user: User = Depends(supplier_managers)):
    return supplier_service.create_supplier(supplier = supplier_in.model_dump())

@router.put("/{code}", response_model = SupplierResponse, status_code = status.HTTP_200_OK)
def update_supplier(code: str, supplier_in: SupplierUpdate, current_user: User = Depends(supplier_managers)):
    return supplier_service.update_supplier(code = code, changes = supplier_in.model_dump(exclude_none = True))

@router.delete("/{code}", status_code = status.HTTP_204_NO_CONTENT)
def delete_supplier(code: str, current_user: User = Depends(supplier_managers)):
    supplier_service.delete_supplier(code = code)
