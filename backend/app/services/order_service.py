from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import OrderRepository, InventoryRepository
from app.schemas.order import OrderCreate, OrderResponse, OrderStatus
from fastapi import HTTPException

class OrderService:
    def __init__(self, db: AsyncSession):
        self.repo = OrderRepository(db)
        self.inventory_repo = InventoryRepository(db) # Cross-domain access via Repo or Service? 
        # Ideally Service calls other Service to keep logic encapsulated.
        # But if circular dependency risk, Repo is safer.
        # Here we just need to check price/stock.

    async def create_order(self, user_id: int, order_in: OrderCreate) -> OrderResponse:
        total_amount = 0.0
        
        # 1. Validate Stock & Calculate Total
        for item in order_in.items:
            product = await self.inventory_repo.get_product(item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            if product.stock_quantity < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
            
            # This is simplified. In real app, we might need to lock rows.
            # But asyncpg + transaction isolation helps.
            
            total_amount += product.price * item.quantity
        
        # 2. Create Order
        order = await self.repo.create_order(user_id, order_in, total_amount)
        
        # 3. Deduct Stock
        for item in order_in.items:
            await self.inventory_repo.update_stock(item.product_id, -item.quantity)
            
        return order

    async def list_orders(self, user_id: int, skip: int = 0, limit: int = 100) -> List[OrderResponse]:
        return await self.repo.list_orders(user_id, skip, limit)

    async def get_order(self, order_id: int) -> Optional[OrderResponse]:
        return await self.repo.get_order(order_id)
        
    async def update_status(self, order_id: int, status: OrderStatus) -> Optional[OrderResponse]:
        return await self.repo.update_status(order_id, status)
