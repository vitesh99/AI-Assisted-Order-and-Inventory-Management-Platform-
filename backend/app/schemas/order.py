from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum
from datetime import datetime
from .product import ProductResponse

class OrderStatus(str, Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderCreate(BaseModel):
    items: List[OrderItemBase]

class OrderItemResponse(OrderItemBase):
    id: int
    price_at_purchase: float
    product: Optional[ProductResponse] = None # Nested product details!
    
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse]
    
    model_config = ConfigDict(from_attributes=True)
