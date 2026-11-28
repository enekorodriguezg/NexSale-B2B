from pydantic import BaseModel, Field

### --------------------------------------------------###

class CatalogItem(BaseModel):
    sku: str
    name: str
    description: str
    category: str
    base_price: float
    stock: int

class CatalogItemUpdate(BaseModel):
    name: str | None = Field(default = None, min_length = 1)
    description: str | None = None
    category: str | None = None
    base_price: float | None = Field(default = None, ge = 0.0)
    stock: int | None = Field(default = None, ge = 0)

class ExportResult(BaseModel):
    exported: int