from pydantic import BaseModel, Field

### --------------------------------------------------###

class CarrierBase(BaseModel):
    name: str = Field(min_length = 1, max_length = 100)
    phone: str = Field(min_length = 6, max_length = 30)
    price_per_shipment: float = Field(ge = 0.0)
    delivery_days: int = Field(ge = 1, le = 60)


class CarrierCreate(CarrierBase):
    code: str = Field(min_length = 1, max_length = 20)


class CarrierUpdate(BaseModel):
    name: str | None = Field(default = None, min_length = 1, max_length = 100)
    phone: str | None = Field(default = None, min_length = 6, max_length = 30)
    price_per_shipment: float | None = Field(default = None, ge = 0.0)
    delivery_days: int | None = Field(default = None, ge = 1, le = 60)


class CarrierResponse(CarrierBase):
    code: str