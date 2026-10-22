from pydantic import BaseModel, Field, ConfigDict, computed_field

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
        elif self.stock < 10:
            return "LOW_STOCK"
        return "IN_STOCK"

    


class ProductUpdate(BaseModel):
    name: str = Field(min_length = 1)
    description: str = Field(min_length = 1)
    base_price: float = Field(ge = 0.0)
    stock: float = Field(ge = 0)

