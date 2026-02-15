from sqlalchemy import Column, Integer, String, Float, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    supplier = relationship("Supplier")

    __table_args__ = (
        CheckConstraint('stock_quantity >= 0', name='check_stock_positive'),
    )

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_email = Column(String)
    phone = Column(String)
    address = Column(String)
    
    # Simple performance metric
    on_time_delivery_rate = Column(Float, default=95.0)

    # Relationship
    # products = relationship("Product", back_populates="supplier")
