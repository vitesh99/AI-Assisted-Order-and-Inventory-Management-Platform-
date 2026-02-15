from fastapi import FastAPI
from app.core.config import settings
from app.auth import routes as auth_routes
from app.db.base import Base
from app.db.session import engine
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=f"{settings.PROJECT_NAME} - Auth Service",
    openapi_url="/api/v1/auth/openapi.json",
    docs_url="/docs/auth"
)

# Include Auth Routes
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Auth Service...")
    # aggregate table creation (for simplicity in microservices without rigorous migration tool usage yet)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created.")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "auth-service"}
