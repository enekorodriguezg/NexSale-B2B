from pydantic import BaseModel, Field, ConfigDict, computed_field

from server.constants import UserRole

### --------------------------------------------------###

class ProductSummary(BaseModel):
    id: int
    name: str
    sku:str
    model_config = ConfigDict(from_attributes=True)


class OrderItemBase(BaseModel):
    quantity: int = Field(ge=1, description = "Quantity must be at least 1")


class OrderItemCreate(OrderItemBase):
    product_id: int = Field(ge=1, description = "Reference to the product")


class OrderItemResponse(OrderItemBase):
    id: int 
    unit_price: float = Field(ge = 0.0, description = "Price frozen at purchase time")
    product: ProductSummary | None = Field(default=None, description = "Product details")

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def total_price(self) -> float:
        return round(self.quantity*self.unit_price,2)

    