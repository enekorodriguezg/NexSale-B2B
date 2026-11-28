from pydantic import BaseModel

### --------------------------------------------------###

class ConvertedPrice(BaseModel):
    currency: str
    rate: float
    price: float


class ProductPrices(BaseModel):
    product_id: int
    name: str
    base_currency: str
    base_price: float
    rates_date: str
    prices: list[ConvertedPrice]