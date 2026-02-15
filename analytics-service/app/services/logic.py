from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func, desc
from app.models.models import Order, OrderItem, Product
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_stats(self):
        # Revenue
        res_rev = await self.db.execute(select(func.sum(Order.total_amount)).where(Order.status != "CANCELLED"))
        total_revenue = res_rev.scalar() or 0.0

        # Status Dist
        res_dist = await self.db.execute(select(Order.status, func.count(Order.id)).group_by(Order.status))
        status_dist = dict(res_dist.all())

        total_orders = sum(status_dist.values())
        pending = status_dist.get("CREATED", 0) + status_dist.get("CONFIRMED", 0)

        # Low Stock
        res_low = await self.db.execute(select(Product).where(Product.stock_quantity < 10))
        low_stock = res_low.scalars().all()
        
        # Top Selling
        stmt = (
            select(Product.id, Product.name, func.sum(OrderItem.quantity).label("total_sold"))
            .join(OrderItem, Product.id == OrderItem.product_id)
            .join(Order, OrderItem.order_id == Order.id)
            .where(Order.status != "CANCELLED")
            .group_by(Product.id, Product.name)
            .order_by(desc("total_sold"))
            .limit(5)
        )
        res_top = await self.db.execute(stmt)
        top_products = [{"id": r.id, "name": r.name, "total_sold": r.total_sold} for r in res_top.all()]

        # Mock Daily Revenue
        daily = {
            "Mon": total_revenue * 0.1, "Tue": total_revenue * 0.2, 
            "Wed": total_revenue * 0.15, "Thu": total_revenue * 0.25, "Fri": total_revenue * 0.3
        }

        return {
            "stats": {
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "pending_orders": pending,
                "low_stock_count": len(low_stock)
            },
            "top_selling_products": top_products,
            "low_stock_products": [{"id": p.id, "name": p.name, "stock_quantity": p.stock_quantity, "price": p.price} for p in low_stock],
            "daily_revenue": daily,
            "order_status_distribution": status_dist
        }
