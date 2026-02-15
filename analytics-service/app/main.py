from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.logic import AnalyticsService, get_db

app = FastAPI(title="Analytics Service")

@app.get("/api/v1/analytics/dashboard")
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    service = AnalyticsService(db)
    return await service.get_stats()

@app.get("/health")
def health():
    return {"status": "ok"}
