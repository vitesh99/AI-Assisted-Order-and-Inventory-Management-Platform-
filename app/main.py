from fastapi import FastAPI
from app.core.config import settings
from app.auth import routes as auth_routes
from app.inventory import routes as inventory_routes
from app.orders import routes as orders_routes
from app.db.base import Base
from app.db.session import engine
from app.core import models # Ensure models are loaded
from app.ai import models as ai_models

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Startup event to create tables (for Phase 1 simplicity)
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Middleware
from app.core.middleware import global_exception_handler
from app.core.request_logging import RequestLogMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.exceptions import AppError

app.add_middleware(RequestLogMiddleware)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(AppError, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, global_exception_handler)

# Ops
from app.core import ops
app.include_router(ops.router, tags=["ops"])

app.include_router(auth_routes.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(inventory_routes.router, prefix=f"{settings.API_V1_STR}/inventory", tags=["inventory"])
app.include_router(orders_routes.router, prefix=f"{settings.API_V1_STR}/orders", tags=["orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Assisted Order and Inventory Management Platform (Phase 1)"}
