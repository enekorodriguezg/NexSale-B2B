from pydantic import BaseModel, Field

### --------------------------------------------------###

EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

### --------------------------------------------------###

class SupplierBase(BaseModel):
    name: str = Field(min_length = 1, max_length = 100)
    contact_person: str = Field(min_length = 1, max_length = 100)
    email: str = Field(pattern = EMAIL_PATTERN)
    phone: str = Field(min_length = 6, max_length = 30)
    category: str = Field(min_length = 1, max_length = 50)

class SupplierCreate(SupplierBase):
    code: str = Field(min_length = 1, max_length = 20)

class SupplierUpdate(BaseModel):
    name: str | None = Field(default = None, min_length = 1, max_length = 100)
    contact_person: str | None = Field(default = None, min_length = 1, max_length = 100)
    email: str | None = Field(default = None, pattern = EMAIL_PATTERN)
    phone: str | None = Field(default = None, min_length = 6, max_length = 30)
    category: str | None = Field(default = None, min_length = 1, max_length = 50)

class SupplierResponse(SupplierBase):
    code: str