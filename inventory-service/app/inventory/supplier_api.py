from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.inventory.models import Supplier
# from app.inventory.supplier_model import Supplier
from pydantic import BaseModel

router = APIRouter()

class SupplierCreate(BaseModel):
    name: str
    contact_email: str | None = None
    phone: str | None = None

class SupplierResponse(SupplierCreate):
    id: int
    on_time_delivery_rate: float

@router.post("/", response_model=SupplierResponse)
async def create_supplier(supplier: SupplierCreate, db: AsyncSession = Depends(get_db)):
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    await db.commit()
    await db.refresh(db_supplier)
    return db_supplier

@router.get("/", response_model=list[SupplierResponse])
async def list_suppliers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Supplier))
    return result.scalars().all()
