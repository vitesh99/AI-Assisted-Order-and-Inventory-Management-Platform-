from pydantic import BaseModel, Field
from typing import Optional, List

class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1)
    contact_email: Optional[str] = None
    phone: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    on_time_delivery_rate: float
    
    class Config:
        from_attributes = True
