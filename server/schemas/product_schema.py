from pydantic import BaseModel, Field, ConfigDict, computed_field

from server.core.app_settings import app_settings

### --------------------------------------------------###

class ProductBase(BaseModel):
    sku: str = Field(min_length = 1)
    name: str = Field(min_length = 1)
    description: str | None = None
    category: str
    base_price: float = Field(ge = 0.0)
    stock: int = Field(ge = 0)

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    @computed_field
    @property
    def inventory_value(self) -> float:
        return round(self.base_price * self.stock, 2)

    @computed_field
    @property
    def stock_status(self) -> str:
        if self.stock == 0:
            return "OUT_OF_STOCK"
        elif self.stock < app_settings.low_stock_threshold:
            return "LOW_STOCK"
        return "IN_STOCK"

class ProductUpdate(BaseModel):
    sku: str | None = Field(default = None, min_length = 1)
    name: str | None = Field(default = None, min_length = 1)
    description: str | None = None
    category: str | None = None
    base_price: float | None = Field(default = None, ge = 0.0)
    stock: int | None = Field(default = None, ge = 0)
