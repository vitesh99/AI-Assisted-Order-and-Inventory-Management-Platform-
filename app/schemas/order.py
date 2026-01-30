from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from .inventory import InventoryItem

class OrderItemCreate(BaseModel):
    inventory_item_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItem(BaseModel):
    id: int
    inventory_item_id: int
    quantity: int
    price_at_purchase: Optional[float] = 0.0 # Placeholder logic for price as it's not in inventory model effectively

    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItem] = []

    class Config:
        from_attributes = True
