from pydantic import BaseModel, Field, ConfigDict

### --------------------------------------------------###

class ProductBase(BaseModel):
    sku: str = Field(min_length = 1)
    name: str = Field(min_length = 1)
    description: str | None = None
    category: str
    base_price: float = Field(ge = 0.0)
    stock: int = Field(ge = 0)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

