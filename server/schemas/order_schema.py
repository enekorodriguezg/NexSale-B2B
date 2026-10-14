from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field

from .order_item_schema import OrderItemCreate, OrderItemResponse
from server.oib_validation import is_valid_oib

### --------------------------------------------------###

class OrderBase(BaseModel):
    customer_name: str
    customer_tax_id: str = Field(min_length=11,max_length=11)

    @field_validator("customer_tax_id")
    @classmethod
    def validate_oib(cls, value: str) -> str:
        if not is_valid_oib(value):
            raise ValueError("Invalid Croatian Tax ID (OIB)")
        return value


class OrderCreate(OrderBase):
    items: list[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    user_id: int
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def order_price(self) -> float:
        order_price = 0.0

        for item in self.items:
            order_price += item.total_price

        return order_price
    

   

