from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import AnalyticsResponse

router = APIRouter()

def get_service(db: AsyncSession = Depends(get_db)) -> AnalyticsService:
    return AnalyticsService(db)

@router.get("/dashboard", response_model=AnalyticsResponse)
async def get_dashboard_metrics(service: AnalyticsService = Depends(get_service)):
    return await service.get_dashboard_stats()
