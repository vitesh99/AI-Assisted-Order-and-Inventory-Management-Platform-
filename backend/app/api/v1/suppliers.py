from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.services.inventory_service import InventoryService # Supplier logic is here for now
from app.schemas.supplier import SupplierCreate, SupplierResponse

router = APIRouter()

def get_service(db: AsyncSession = Depends(get_db)) -> InventoryService:
    return InventoryService(db)

@router.post("/", response_model=SupplierResponse)
async def create_supplier(supplier: SupplierCreate, service: InventoryService = Depends(get_service)):
    return await service.create_supplier(supplier)

@router.get("/", response_model=List[SupplierResponse])
async def list_suppliers(skip: int = 0, limit: int = 100, service: InventoryService = Depends(get_service)):
    return await service.list_suppliers(skip, limit)
