from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from server.schemas.order_schema import OrderCreate
from server.models import Order, Product, User, OrderItem

### --------------------------------------------------###

def create_order(db: Session, order_data: OrderCreate, user_id: int) -> Order:

    try:
        running_total = 0.0
        db_items: list[OrderItem] = []

        sorted_items = sorted(order_data.items, key=lambda x: x.product_id) #For safer locking during coocurring transactions

        for item in sorted_items:
            stmt = (select(Product).where(Product.id == item.product_id).with_for_update())
            product = db.execute(stmt).scalar_one_or_none()

            if not product:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = f"Product with ID {item.product_id} not found"
                )
            current_stock = int(product.stock) #type: ignore

            if int(current_stock) < item.quantity:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = (
                        f"Insufficient stock for '{product.name}' ID: {product.id}"
                        f"Available: {product.stock}, requested: {item.quantity}"
                    )
                )

            #Update stock
            product.stock -= item.quantity #type: ignore

            #Subtotal update
            running_total += item.quantity*product.base_price

            #Item creation in memory
            order_item = OrderItem(
                product_id = product.id,
                quantity = item.quantity,
                unit_price = product.base_price
            )
            db_items.append(order_item)

        #Order creation
        new_order = Order(
            user_id = user_id,
            customer_name = order_data.customer_name,
            customer_tax_id = order_data.customer_tax_id,
            base_total = running_total,
            items = db_items,
        )

        #DataBase Update
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return new_order

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An unexpected error occurred while processing the order"
        ) from e

    
