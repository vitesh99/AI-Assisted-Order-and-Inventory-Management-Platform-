from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.base import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    contact_email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    
    # Performance Metrics
    on_time_delivery_rate = Column(Float, default=100.0) # Percentage
    
    products = relationship("Product", back_populates="supplier")
