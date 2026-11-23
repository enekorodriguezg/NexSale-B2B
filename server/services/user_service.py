from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from server.models import User

### --------------------------------------------------###

def get_user_by_id(user_id: int, db: Session) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()

### --------------------------------------------------###

def get_all_users(order_by: str, sort_order: str, db: Session) -> list[User]:
    allowed_columns : list[str] = ["id", "name", "base_price", "stock"]
    if order_by not in allowed_columns:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid column for order"
        )

    sort_column = getattr(User, order_by)
    if sort_order.lower() == "desc":
        sort_criteria = sort_column.desc()
    
    else:
        sort_criteria = sort_column.asc()

    stmt = select(User).order_by(sort_criteria)
    return list(db.scalars(stmt).all())