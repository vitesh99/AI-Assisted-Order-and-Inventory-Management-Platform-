from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, case
from app.models import Order, OrderItem, Product, OrderStatus

class AnalyticsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_total_revenue(self) -> float:
        result = await self.db.execute(
            select(func.sum(Order.total_amount))
            .where(Order.status != OrderStatus.CANCELLED.value)
        )
        return result.scalar() or 0.0

    async def get_top_selling_products(self, limit: int = 5):
        # Group by product, sum quantity
        stmt = (
            select(Product.id, Product.name, func.sum(OrderItem.quantity).label("total_sold"))
            .join(OrderItem, Product.id == OrderItem.product_id)
            .join(Order, OrderItem.order_id == Order.id)
            .where(Order.status != OrderStatus.CANCELLED.value)
            .group_by(Product.id, Product.name)
            .order_by(desc("total_sold"))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.all()

    async def get_low_stock_products(self, threshold: int = 10):
        result = await self.db.execute(
            select(Product)
            .where(Product.stock_quantity < threshold)
            .order_by(Product.stock_quantity)
        )
        return result.scalars().all()

    async def get_order_status_distribution(self):
        result = await self.db.execute(
            select(Order.status, func.count(Order.id))
            .group_by(Order.status)
        )
        return dict(result.all())
