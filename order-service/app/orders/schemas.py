from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class OrderStatus(str, Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    FULFILLED = "FULFILLED"
    CANCELLED = "CANCELLED"

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderCreate(BaseModel):
    items: List[OrderItemBase]

class OrderItemResponse(OrderItemBase):
    id: int
    price_at_purchase: float
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_amount: float
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True
