from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.base import Base

class OrderStatus(str, enum.Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"     # New status
    DELIVERED = "DELIVERED" # New status
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String, default=OrderStatus.CREATED.value, nullable=False, index=True)
    total_amount = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    ai_metadata = relationship("OrderAIMetadata", back_populates="order", uselist=False, cascade="all, delete-orphan")
    
    # For Analytics queries
    user = relationship("User") 

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product") # Direct relationship restored!

class OrderAIMetadata(Base):
    __tablename__ = "order_ai_metadata"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    summary_text = Column(Text, nullable=True)
    notification_draft = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    order = relationship("Order", back_populates="ai_metadata")
