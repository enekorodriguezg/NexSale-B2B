from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):

    __tablename__="user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    salt = Column(String(64), nullable=False)
    role = Column(String(20), default="commercial", nullable=False)


class Product(Base):

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    base_price = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)

    #Relationship to order items
    order_items=relationship("OrderItem",back_populates="product")


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    customer_tax_id = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(20), default="Pending", nullable=False)
    base_total = Column(Float, default=0.0, nullable=False)

    #Relationship to items
    items = relationship("OrderItem", back_populates="order", cascade="all,delete-orphan")



class OrderItem(Base):

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Float, default=0.0, nullable=False)

    #Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
