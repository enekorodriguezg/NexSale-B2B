from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from .database import Base

### --------------------------------------------------###

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(50), unique = True, nullable = False, index = True)
    hashed_password = Column(String(255), nullable = False)
    salt = Column(String(64), nullable = False)
    role = Column(String(20), default = "commercial", nullable = False)
    orders = relationship("Order", back_populates = "user") #Relationship to order


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key = True, index = True)
    sku = Column(String(50), unique = True, nullable = False, index = True)
    name = Column(String(50), nullable = False)
    description = Column(String(100), nullable = False)
    category = Column(String(50), nullable = False, index = True)
    base_price = Column(Float, nullable = False)
    stock = Column(Integer, default = 0, nullable = False)
    order_items = relationship("OrderItem",back_populates = "product") #Relationship to order items

    def has_enough_stock(self, quantity: int) -> bool:
        return self.stock >= quantity #type: ignore

    def reduce_stock(self, quantity: int) -> None:
        self.stock -= quantity



class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_name = Column(String(100), nullable = False)
    customer_tax_id = Column(String(20), nullable = False)
    created_at = Column(DateTime, default = datetime.now(timezone.utc), nullable = False)
    status = Column(String(20), default = "Pending", nullable = False)
    base_total = Column(Float, default = 0.0, nullable = False)
    items = relationship("OrderItem", back_populates = "order", cascade = "all,delete-orphan") #Relationship 1
    user = relationship("User", back_populates = "orders") #Relationship 2

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

    id = Column(Integer, primary_key = True, index = True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable = False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable = False)
    quantity = Column(Integer, default = 1, nullable = False)
    unit_price = Column(Float, default = 0.0, nullable = False)
    order = relationship("Order", back_populates = "items") #Relationship 1
    product = relationship("Product", back_populates = "order_items") #Relationship 2

    def is_product(self, id: int) -> bool:
        return id == self.product_id

    def calculate_subtotal(self) -> float:
        return round(self.unit_price * self.quantity,2) #type: ignore
