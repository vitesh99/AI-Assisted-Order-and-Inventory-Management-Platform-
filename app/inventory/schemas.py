from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0, description="Price must be greater than zero")
    stock_quantity: int = Field(ge=0, description="Stock must be non-negative")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
