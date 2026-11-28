from fastapi import APIRouter, status, Depends

from server.api.deps import RoleChecker
from server.constants import UserRole
from server.models import User
from server.schemas.carrier_schema import CarrierResponse, CarrierCreate, CarrierUpdate
from server.services import carrier_service

### --------------------------------------------------###

router = APIRouter(prefix = "/carriers", tags = ["Carriers"])

all_roles = RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE, UserRole.COMMERCIAL])
carrier_managers = RoleChecker([UserRole.ADMIN, UserRole.WAREHOUSE])

### --------------------------------------------------###

@router.get("", response_model = list[CarrierResponse], status_code = status.HTTP_200_OK)
def get_carriers(current_user: User = Depends(all_roles)):
    return carrier_service.get_carriers()

@router.post("", response_model = CarrierResponse, status_code = status.HTTP_201_CREATED)
def create_carrier(carrier_in: CarrierCreate, current_user: User = Depends(carrier_managers)):
    return carrier_service.create_carrier(carrier = carrier_in.model_dump())

@router.put("/{code}", response_model = CarrierResponse, status_code = status.HTTP_200_OK)
def update_carrier(code: str, carrier_in: CarrierUpdate, current_user: User = Depends(carrier_managers)):
    return carrier_service.update_carrier(code = code, changes = carrier_in.model_dump(exclude_none = True))

@router.delete("/{code}", status_code = status.HTTP_204_NO_CONTENT)
def delete_carrier(code: str, current_user: User = Depends(carrier_managers)):
    carrier_service.delete_carrier(code = code)