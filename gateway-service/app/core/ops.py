from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db
import time
import psutil
import os

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Check DB connection
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "detail": str(e)}

@router.get("/metrics")
async def get_metrics():
    process = psutil.Process(os.getpid())
    return {
        "uptime": time.time() - process.create_time(),
        "memory_usage_mb": process.memory_info().rss / 1024 / 1024,
        "cpu_percent": process.cpu_percent(),
        # Add request counts from middleware if implementing a counter there
    }
