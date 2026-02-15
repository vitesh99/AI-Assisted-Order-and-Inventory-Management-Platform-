from fastapi import FastAPI
from app.orders.api import router as orders_router

app = FastAPI(title="Order Service")

app.include_router(orders_router, prefix="/api/v1/orders", tags=["orders"])

@app.on_event("startup")
async def startup_event():
    from app.db.session import engine
    from app.db.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
def health():
    return {"status": "ok"}
