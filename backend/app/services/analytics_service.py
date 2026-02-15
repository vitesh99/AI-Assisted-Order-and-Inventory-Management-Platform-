from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import AnalyticsRepository
from app.schemas.analytics import AnalyticsResponse, DashboardStats, TopProduct, LowStockProduct
from datetime import datetime

class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.repo = AnalyticsRepository(db)

    async def get_dashboard_stats(self) -> AnalyticsResponse:
        total_revenue = await self.repo.get_total_revenue()
        status_dist = await self.repo.get_order_status_distribution()
        
        total_orders = sum(status_dist.values())
        pending_orders = status_dist.get("CREATED", 0) + status_dist.get("CONFIRMED", 0)
        
        top_products_raw = await self.repo.get_top_selling_products()
        top_products = [
            TopProduct(id=r.id, name=r.name, total_sold=r.total_sold) 
            for r in top_products_raw
        ]
        
        low_stock_raw = await self.repo.get_low_stock_products()
        low_stock = [
            LowStockProduct(id=p.id, name=p.name, stock_quantity=p.stock_quantity, price=p.price)
            for p in low_stock_raw
        ]
        
        stats = DashboardStats(
            total_revenue=total_revenue,
            total_orders=total_orders,
            pending_orders=pending_orders,
            low_stock_count=len(low_stock)
        )
        
        # Mock daily revenue for chart (until we implement real time-series query)
        daily_revenue = {
            "Mon": total_revenue * 0.1,
            "Tue": total_revenue * 0.2,
            "Wed": total_revenue * 0.15,
            "Thu": total_revenue * 0.25,
            "Fri": total_revenue * 0.3
        }
        
        return AnalyticsResponse(
            stats=stats,
            top_selling_products=top_products,
            low_stock_products=low_stock,
            daily_revenue=daily_revenue,
            order_status_distribution=status_dist
        )
