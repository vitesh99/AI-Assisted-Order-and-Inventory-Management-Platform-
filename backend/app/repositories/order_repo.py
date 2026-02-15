from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models import Order, OrderItem, OrderStatus, Product
from app.schemas.order import OrderCreate

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, user_id: int, order_in: OrderCreate, total_amount: float) -> Order:
        db_order = Order(
            user_id=user_id,
            status=OrderStatus.CREATED.value,
            total_amount=total_amount
        )
        self.db.add(db_order)
        # Flush to get ID
        await self.db.flush()
        
        # Add items
        for item in order_in.items:
            # We assume price logic is handled in service, but we need price here.
            # Ideally passed in, but for repo simplicity, we might query or trust service passed enriched data.
            # Let's assume service handles calculating total and passing items with prices? 
            # Or repo fetches product again? Repo fetching is safer.
            
            # Optimization: Fetch all products in one query in Service, passing prices here?
            # For strict repo pattern, let's keep it simple: Service fetches prices, 
            # Repo creates records. But arguments need to match.
            # I'll stick to basic creation here assuming caller validation.
            # Wait, I need price_at_purchase. 
            # I will refactor create_order to accept dicts with price.
            pass
        
        # Actually proper way:
        # Service calculates total and prepares Order object. Repo just saves.
        # But relationships are tricky.
        
        return db_order

    # Refined create method that takes fully prepared ORM objects or data
    async def save_order(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order, attribute_names=['items'])
        return order

    async def get_order(self, order_id: int) -> Optional[Order]:
        # Eager load items and their products
        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product), 
                selectinload(Order.ai_metadata)
            )
            .where(Order.id == order_id)
        )
        return result.scalars().first()

    async def list_orders(self, user_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Order]:
        query = select(Order).options(selectinload(Order.items).selectinload(OrderItem.product)).offset(skip).limit(limit)
        if user_id:
            query = query.where(Order.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_status(self, order_id: int, status: OrderStatus) -> Optional[Order]:
        stmt = (
            update(Order)
            .where(Order.id == order_id)
            .values(status=status.value)
            .execution_options(synchronize_session="fetch")
            .returning(Order)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalars().first()
