from pydantic import BaseModel, Field, ConfigDict, field_validator
from .order_item_schema import OrderItemCreate
from server.oib_validation import is_valid_oib


class OrderBase(BaseModel):
    customer_name: str
    customer_tax_id: int = Field(min_length=11,max_length=11)

    @field_validator("customer_tax_id")
    @classmethod
    def validate_oib(cls, value: int)->int:
        if not is_valid_oib(value):
            raise ValueError("Invalid Croatian Tax ID (OIB)")
        return value


class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    

    model_config = ConfigDict(from_attributes=True)

