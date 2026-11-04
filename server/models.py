from sqlalchemy import String, ForeignKey, LargeBinary, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone

from .database import Base

### --------------------------------------------------###

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    username: Mapped[str] = mapped_column(String(50), unique = True, nullable = False, index = True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable = False)
    salt: Mapped[str] = mapped_column(String(64), nullable = False)
    role: Mapped[str] = mapped_column(String(20), default = "commercial", nullable = False)
    orders = relationship("Order", back_populates = "user") #Relationship to order


class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    sku: Mapped[str] = mapped_column(String(50), unique = True, nullable = False, index = True)
    name: Mapped[str] = mapped_column(String(50), nullable = False)
    description: Mapped[str] = mapped_column(String(100), nullable = False)
    category: Mapped[str] = mapped_column(String(50), nullable = False, index = True)
    base_price: Mapped[float] = mapped_column(nullable = False)
    stock: Mapped[int] = mapped_column(default = 0, nullable = False)
    image: Mapped[bytes | None] = mapped_column(LargeBinary, nullable = True)
    order_items = relationship("OrderItem",back_populates = "product")

    def has_enough_stock(self, quantity: int) -> bool:
        return self.stock >= quantity

    def reduce_stock(self, quantity: int) -> None:
        self.stock -= quantity



class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    customer_name: Mapped[str] = mapped_column(String(100), nullable = False)
    customer_tax_id: Mapped[str] = mapped_column(String(20), nullable = False)
    created_at: Mapped[datetime] = mapped_column(server_default = func.now(), nullable = False)
    status: Mapped[str] = mapped_column(String(20), default = "Pending", nullable = False)
    base_total: Mapped[float] = mapped_column(default = 0.0, nullable = False)
    items = relationship("OrderItem", back_populates = "order", cascade = "all,delete-orphan")
    user = relationship("User", back_populates = "orders")

    def calculate_total(self) -> float:
        new_total = 0.0
        for item in self.items:
            new_total += item.calculate_subtotal()
        self.base_total = new_total
        return self.base_total

    def get_num_of_items(self) -> int:
        return sum(item.quantity for item in self.items)



class OrderItem(Base):

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable = False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable = False)
    quantity: Mapped[int] = mapped_column(default = 1, nullable = False)
    unit_price: Mapped[float] = mapped_column(default = 0.0, nullable = False)
    order = relationship("Order", back_populates = "items")
    product = relationship("Product", back_populates = "order_items")

    def is_product(self, id: int) -> bool:
        return id == self.product_id

    def calculate_subtotal(self) -> float:
        return round(self.unit_price * self.quantity,2)
