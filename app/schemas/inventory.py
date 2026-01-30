from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class InventoryItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    quantity: int = 0

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemUpdate(BaseModel):
    quantity: int

class InventoryItem(InventoryItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
