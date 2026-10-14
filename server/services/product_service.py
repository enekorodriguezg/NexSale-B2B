from sqlalchemy.orm import Session
from sqlalchemy import select

from server.models import Product

### --------------------------------------------------###

def get_all_products(db: Session) -> list[Product]:
    stmt = select(Product)
    return list(db.scalars(stmt).all())