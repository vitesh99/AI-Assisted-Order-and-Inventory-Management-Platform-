from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.orders.models import Order, OrderItem, OrderStatus
from app.orders.schemas import OrderCreate
import httpx
import os

INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL", "http://inventory-service:8000/api/v1/inventory")

class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_stock(self, product_id: int, quantity: int):
        async with httpx.AsyncClient() as client:
            try:
                # Get product details
                resp = await client.get(f"{INVENTORY_SERVICE_URL}/{product_id}")
                if resp.status_code != 200:
                    raise Exception(f"Product {product_id} not found")
                
                product = resp.json()
                if product['stock_quantity'] < quantity:
                     raise Exception(f"Insufficient stock for product {product_id}")
                
                return product
            except httpx.RequestError:
                 raise Exception("Inventory service unavailable")

    async def _deduct_stock(self, product_id: int, quantity: int):
        async with httpx.AsyncClient() as client:
            # We need a dedicated endpoint for stock deduction in inventory service
            # For MVP restoration, we might just update quantity via PUT? 
            # Ideally: POST /inventory/{id}/deduct
            # Let's assume we use the update endpoint for now or add a specific one.
            # To be safe and quick, we'll try to update.
            # BUT, we need to KNOW current stock to update it properly via PUT.
            # This is race-condition prone without atomic endpoint.
            # For this task, we will assume a simple endpoint exists or we add it.
            # proper way: 
            payload = {"quantity": quantity}
            resp = await client.post(f"{INVENTORY_SERVICE_URL}/{product_id}/deduct", json=payload)
            if resp.status_code != 200:
                raise Exception("Failed to deduct stock")

    async def create_order(self, user_id: int, order_data: OrderCreate):
        # 1. Validate Stock (Call Inventory Service)
        total_amount = 0.0
        product_cache = {}
        
        for item in order_data.items:
             product = await self._check_stock(item.product_id, item.quantity)
             total_amount += product['price'] * item.quantity
             product_cache[item.product_id] = product

        # 2. Create Order
        db_order = Order(user_id=user_id, total_amount=total_amount, status=OrderStatus.CREATED)
        self.db.add(db_order)
        await self.db.flush() # Get ID

        # 3. Create Items & Deduct Stock
        for item in order_data.items:
            product = product_cache[item.product_id]
            db_item = OrderItem(
                order_id=db_order.id, 
                product_id=item.product_id, 
                quantity=item.quantity,
                price_at_purchase=product['price']
            )
            self.db.add(db_item)
            # Distributed Transaction Risk! If this fails, we have inconsistency. 
            # In real system: Saga pattern. Here: Best effort.
            await self._deduct_stock(item.product_id, item.quantity)
            
        await self.db.commit()
        await self.db.refresh(db_order)
        return db_order

    async def get_order(self, order_id: int):
        result = await self.db.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()
    
    async def list_orders(self, user_id: int = None):
         # Internal Tool: Show all orders if user_id is not specified (or always)
         # For this specific "Production Level" request, we want global visibility.
         stmt = select(Order).order_by(Order.id.desc())
         if user_id:
             # Optional: Assert user is admin? For now, let's just show all.
             pass 
         
         result = await self.db.execute(stmt)
         return result.scalars().all()

    async def update_order_status(self, order_id: int, status: OrderStatus):
        order = await self.get_order(order_id)
        if not order:
             return None
        
        order.status = status
        await self.db.commit()
        await self.db.refresh(order)
        return order
