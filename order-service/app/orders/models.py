from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base

class OrderStatus(str, enum.Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    FULFILLED = "FULFILLED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True) # ForeignKey("users.id") Removed for microservices
    status = Column(String, default=OrderStatus.CREATED.value, nullable=False, index=True)
    total_amount = Column(Float, default=0.0)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="selectin")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, nullable=False, index=True) # ForeignKey("products.id") Removed for microservices
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
