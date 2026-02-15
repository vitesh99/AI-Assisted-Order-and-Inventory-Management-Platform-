from fastapi import FastAPI
from app.inventory.api import router as inventory_router
# We will create supplier router next
from app.inventory.supplier_api import router as supplier_router

app = FastAPI(title="Inventory Service")

app.include_router(inventory_router, prefix="/api/v1/inventory", tags=["inventory"])
app.include_router(supplier_router, prefix="/api/v1/suppliers", tags=["suppliers"])

@app.on_event("startup")
async def startup_event():
    from app.db.session import engine
    from app.db.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
def health():
    return {"status": "ok"}
