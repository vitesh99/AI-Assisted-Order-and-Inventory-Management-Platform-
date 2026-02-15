from pydantic import BaseModel
from typing import List, Dict

class TopProduct(BaseModel):
    id: int
    name: str
    total_sold: int

class LowStockProduct(BaseModel):
    id: int
    name: str
    stock_quantity: int
    price: float

class DashboardStats(BaseModel):
    total_revenue: float
    total_orders: int
    pending_orders: int
    low_stock_count: int
    
class AnalyticsResponse(BaseModel):
    stats: DashboardStats
    top_selling_products: List[TopProduct]
    low_stock_products: List[LowStockProduct]
    daily_revenue: Dict[str, float] # Date -> Amount
    order_status_distribution: Dict[str, int]
